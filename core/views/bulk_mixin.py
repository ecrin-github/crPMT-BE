from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class BulkModelMixin:
    """
    Bulk create / update / delete actions for ModelViewSets, to save a list of items in a single query
    instead of one query per item.

    The view's get_serializer_class must return the input serializer for the bulk_create and bulk_update actions,
    responses are serialized with the view's serializer_class (output serializer), in the same order as the payload.
    Views whose output serializer renders nested objects can override get_output_queryset to load them in a few queries,
    or set bulk_output_serializer_class to answer with a lighter serializer.
    """

    # Serializer of the bulk responses, the view's serializer_class if None (#125)
    bulk_output_serializer_class = None

    def get_output_queryset(self):
        """Queryset used to reload the saved items before serializing the response, None to serialize them as is (#125)"""
        return None

    def serialize_output(self, instances):
        output_queryset = self.get_output_queryset()
        if output_queryset is not None:
            loaded = output_queryset.in_bulk([instance.pk for instance in instances])
            instances = [loaded[instance.pk] for instance in instances]
        output_serializer_class = self.bulk_output_serializer_class or self.serializer_class
        return output_serializer_class(instances, many=True).data

    @action(methods=["post"], detail=False)
    @transaction.atomic
    def bulk_create(self, request):
        if not isinstance(request.data, list):
            return Response(
                {"detail": "Expected a list of objects"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        instances = serializer.save()
        return Response(self.serialize_output(instances), status=status.HTTP_201_CREATED)

    @action(methods=["put", "patch"], detail=False)
    @transaction.atomic
    def bulk_update(self, request):
        if not isinstance(request.data, list):
            return Response(
                {"detail": "Expected a list of objects"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        partial = request.method == "PATCH"
        errors = {}

        # Fetching all the items in a single query instead of one per item
        pks = [item.get("id") for item in request.data if isinstance(item, dict)]
        objs = self.get_queryset().in_bulk([pk for pk in pks if isinstance(pk, int)])

        # Validating every item before saving any, so that an invalid item doesn't leave the others half saved
        serializers = []
        for idx, item in enumerate(request.data):
            if not isinstance(item, dict):
                errors[idx] = {"detail": ["Expected an object."]}
                continue

            pk = item.get("id")
            if pk is None:
                errors[idx] = {"id": ["This field is required for bulk update."]}
                continue

            obj = objs.get(pk)
            if obj is None:
                errors[idx] = {"id": ["Object not found."]}
                continue

            serializer = self.get_serializer(obj, data=item, partial=partial)
            if serializer.is_valid():
                serializers.append(serializer)
            else:
                errors[idx] = serializer.errors

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        instances = [serializer.save() for serializer in serializers]
        return Response(self.serialize_output(instances))

    @action(methods=["post"], detail=False)
    @transaction.atomic
    def bulk_delete(self, request):
        pks = request.data.get("ids") if isinstance(request.data, dict) else None
        if not isinstance(pks, list) or not all(isinstance(pk, int) for pk in pks):
            return Response(
                {"detail": "Expected an object with a list of ids"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = self.get_queryset().filter(pk__in=pks)
        missing_pks = set(pks) - set(queryset.values_list("pk", flat=True))
        if missing_pks:
            return Response(
                {"ids": [f"Objects not found: {sorted(missing_pks)}"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
