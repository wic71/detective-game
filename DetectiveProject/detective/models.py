from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
    Group,
    Permission,
)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    # Överlagra grupper och permissions med unika related_name
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="customuser_set"  # ändrat från standard "user_set"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_user_set"  # ändrat från standard "user_set"
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Inga extra krav

    def __str__(self):
        return self.email
    
# detective/models.py
from django.db import models
from django.utils import timezone
from django.conf import settings

# --- PLAYER MODEL ---
class Player(models.Model):
    fk_account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="player_profile"
    )
    in_game_first_name = models.CharField(max_length=50)
    in_game_last_name  = models.CharField(max_length=50)
    title              = models.CharField(max_length=50, default='Aspirant')
    avatar_url         = models.CharField(max_length=255)
    sign_up_date       = models.DateTimeField(default=timezone.now)
    num_of_logins      = models.IntegerField(default=1)
    last_login_date    = models.DateTimeField(default=timezone.now)
    fk_current_case_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} {self.in_game_first_name} {self.in_game_last_name}"

# --- CASE TYPE MODEL ---
class CaseType(models.Model):
    name          = models.CharField("Case Type", max_length=255)
    description   = models.TextField("Description", blank=True)
    criminal_person_type    = models.CharField(max_length=255, blank=True)
    criminal_location_type  = models.CharField(max_length=255, blank=True)
    criminal_item_type      = models.CharField(max_length=255, blank=True)
    criminal_mastermind_type      = models.CharField(max_length=255, blank=True)
    criminal_victim_type      = models.CharField(max_length=255, blank=True)


    def __str__(self):
        return self.name

# --- CASCADE ORDER: Place, Person, Item, Dialog, Case ---
class Place(models.Model):
    case = models.ForeignKey(
        'Case',
        on_delete=models.CASCADE,
        related_name='places',
        null=True,
        blank=True
    )
    name                 = models.CharField(max_length=200)
    description          = models.TextField(blank=True)
    deep_description     = models.TextField(blank=True)
    map_x                = models.IntegerField()
    map_y                = models.IntegerField()
    extra_travel_time    = models.IntegerField(default=0)
    image_url            = models.URLField(blank=True)
    is_locked            = models.BooleanField(default=False)
    required_key_item    = models.ForeignKey(
        'Item', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='places_requiring_key_item'
    )
    time_to_examine      = models.IntegerField(default=0)
    time_to_deep_exam    = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Person(models.Model):
    case = models.ForeignKey(
        'Case',
        on_delete=models.CASCADE,
        related_name='persons',
        null=True,
        blank=True
    )
    place               = models.ForeignKey('Place', on_delete=models.SET_NULL, null=True, blank=True)
    name                = models.CharField(max_length=50)
    description         = models.TextField(blank=True)
    image_url           = models.CharField(
        "Person Image URL",
        max_length=255,
        blank=True,
        help_text="Relativ sökväg under static/, ex: detective/images/cases/1/.png"
    )
    initial_attitude    = models.IntegerField(default=50)
    is_criminal         = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Item(models.Model):
    case = models.ForeignKey(
        'Case',
        on_delete=models.CASCADE,
        related_name='items',
        null=True,
        blank=True
    )
    name                  = models.CharField(max_length=200)
    description           = models.TextField(blank=True)
    deep_description      = models.TextField(blank=True)
    image_url             = models.CharField(
        "Item Image URL",
        max_length=255,
        blank=True,
        help_text="Relativ sökväg under static/, ex: detective/images/cases/1/item_x.png"
    )
    evidence_value        = models.IntegerField(default=0)
    time_to_examine       = models.IntegerField(default=0)
    time_to_deep_exam     = models.IntegerField(default=0)
    place                 = models.ForeignKey('Place', on_delete=models.SET_NULL, null=True, blank=True)
    person                = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True, blank=True)
    require_deep_search   = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Dialog(models.Model):
    case = models.ForeignKey(
        'Case',
        on_delete=models.CASCADE,
        related_name='dialogs',
        null=True,      # gör fältet valfritt i databasen
       blank=True      # gör fältet valfritt i formulär/admin
    )
    person                 = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='dialogs')
    node_key               = models.CharField(max_length=100)
    text                   = models.TextField()
    is_entry_node          = models.BooleanField(default=False)
    emotion_above          = models.IntegerField(default=100)
    emotion_below          = models.IntegerField(default=0)
    visit_count            = models.IntegerField(default=0)
    is_evidence            = models.BooleanField(default=False)
    hint_person            = models.ForeignKey(
        'Person', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='hinted_in_dialogs'
    )
    evidence_item          = models.ForeignKey(
        'Item', on_delete=models.SET_NULL, null=True, blank=True
    )
    reaction_description   = models.TextField(blank=True)
    time_for_option        = models.IntegerField(default=1)
    requires_visits        = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.person.name}: {self.node_key}"

class Case(models.Model):
    case_name            = models.CharField("Case Name", max_length=255)
    notebook_description = models.TextField("Notebook Description")
    initial_description  = models.TextField("Initial Description")
    initial_person       = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name='cases_given', verbose_name='Initial Person'
    )
    first_dialogue       = models.ForeignKey(
        Dialog, on_delete=models.CASCADE, related_name='start_cases', verbose_name='First Dialogue'
    )
    notebook_image_url   = models.CharField(
        "Notebook Image URL",
        max_length=255,
        blank=True,
        help_text="Relativ sökväg under static/, ex: detective/images/cases/1/notebook.png"
    )
    intro_image_url      = models.CharField(
        "Intro Image URL",
        max_length=255,
        blank=True,
        help_text="Relativ sökväg under static/, ex: detective/images/cases/1/intro.png"
    )
    case_order           = models.IntegerField("Order")
    case_difficulty      = models.IntegerField("Difficulty")
    is_active            = models.BooleanField("Active", default=True)
    created_at           = models.DateTimeField("Created", default=timezone.now)
    criminal_person      = models.ForeignKey(
        Person, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='criminal_in_cases', verbose_name='Criminal'
    )
    criminal_item        = models.ForeignKey(
        Item, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='cases_with_crime_item', verbose_name='Crime Item'
    )
    criminal_place       = models.ForeignKey(
        Place, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='cases_with_crime_place', verbose_name='Crime Location'
    )
    case_type            = models.ForeignKey(
        CaseType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Case Type'
    )
    mastermind_person    = models.ForeignKey(
        Person, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='mastermind_in_cases', verbose_name='Mastermind'
    )
    victim_person        = models.ForeignKey(
        Person, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='victim_in_cases', verbose_name='Victim'
    )

    def __str__(self):
        return self.case_name
    

class DialogOption(models.Model):
    dialog = models.ForeignKey(
        'detective.Dialog',
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name='Dialog'
    )
    attitude_above = models.IntegerField(
        default=100,
        verbose_name='Attitude Above',
        help_text='Maximal attitydnivå för att alternativet ska visas'
    )
    attitude_below = models.IntegerField(
        default=0,
        verbose_name='Attitude Below',
        help_text='Minsta attitydnivå för att alternativet ska visas'
    )
    item = models.ForeignKey(
        'detective.Item',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dialog_options',
        verbose_name='Required Item'
    )
    person = models.ForeignKey(
        'detective.Person',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dialog_options',
        verbose_name='Required Person'
    )
    place = models.ForeignKey(
        'detective.Place',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dialog_options',
        verbose_name='Required Place'
    )
    option_text = models.TextField(
        verbose_name='Option Text'
    )
    attitude_change = models.IntegerField(
        default=0,
        verbose_name='Attitude Change',
        help_text='Förändring i personens attityd (-100 till 100)'
    )
    next_dialog = models.ForeignKey(
        'detective.Dialog',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='previous_options',
        verbose_name='Next Dialogue'
    )

    def __str__(self):
        return f"Option for {self.dialog.node_key}: {self.option_text[:30]}..."