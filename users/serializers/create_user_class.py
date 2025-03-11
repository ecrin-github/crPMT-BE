class CreateUserDto:
    # LS AAI Fields
    email: str  # also user view field
    sub: str
    name: str
    family_name: str

    # User view fields
    first_name: str
    last_name: str
    is_superuser: bool

    def __init__(self, sub, name, family_name, email, 
                first_name, last_name, is_superuser):
        self.email = email
        self.name = name
        self.sub = sub
        self.family_name = family_name

        self.first_name = first_name
        self.last_name = last_name
        self.is_superuser = is_superuser
