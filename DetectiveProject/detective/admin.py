from django.contrib import admin

from .models import Case, Person, Item, Place, CaseType, Dialog, DialogOption

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = (
        'case_name', 'case_order', 'case_difficulty', 'is_active', 'created_at',
        'initial_person', 'criminal_person', 'case_type'
    )
    list_filter = ('is_active', 'case_difficulty', 'case_type')
    search_fields = ('case_name', 'notebook_description', 'initial_description')
    ordering = ('case_order',)
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('case_name', 'case_order', 'case_difficulty', 'is_active')
        }),
        ('Descriptions', {
            'fields': ('notebook_description', 'initial_description')
        }),
        ('Images', {
            'fields': ('notebook_image_url', 'intro_image_url')
        }),
        ('Participants & Relations', {
            'fields': (
                'initial_person', 'first_dialogue', 'case_type',
                'criminal_person', 'criminal_item', 'criminal_place',
                'mastermind_person', 'victim_person'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    # Vilka kolumner som syns i listvyn
    list_display = (
        'name',
        'case',
        'place',
        'initial_attitude',
        'is_criminal',
    )
    # Filter i sidopanelen
    list_filter = (
        'case',
        'is_criminal',
    )
    # Sökfält över angivna fält
    search_fields = (
        'name',
        'description',
    )
    # För FK-fält kan man använda raw_id_fields för snabb navigering
    raw_id_fields = (
        'case',
        'place',
    )
    # Logisk grupperad inmatningsvy
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'image_url',
                'description',
            ),
        }),
        ('Placering & Roll', {
            'fields': (
                'case',
                'place',
                'initial_attitude',
                'is_criminal',
            ),
            'description': 'Var personen hör hemma i fallet, känsloläge och om de är misstänkta.',
        }),
    )
    # Gör vissa fält read-only om du vill (t.ex. beräknade fält)
    readonly_fields = ()

    
@admin.register(CaseType)
class CaseTypeAdmin(admin.ModelAdmin):
    list_display  = ('name', 'criminal_person_type', 'criminal_location_type', 'criminal_item_type')
    search_fields = ('name', 'description')
    fieldsets = (
        (None, {
            'fields': ('name', 'description'),
        }),
        ('Terminologi', {
            'fields': ('criminal_person_type', 'criminal_location_type', 'criminal_item_type'),
            'description': 'Anpassade benämningar för denna typ av fall.',
        }),
    )


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display  = ('name', 'case', 'map_x', 'map_y', 'is_locked')
    list_filter   = ('case', 'is_locked')
    search_fields = ('name', 'description', 'deep_description')
    raw_id_fields = ('case', 'required_key_item')
    fieldsets = (
        (None, {
            'fields': ('name', 'case', 'image_url', 'is_locked'),
        }),
        ('Beskrivning', {
            'fields': ('description', 'deep_description'),
        }),
        ('Karta & Resa', {
            'fields': ('map_x', 'map_y', 'extra_travel_time'),
        }),
        ('Examinerings‑inställningar', {
            'fields': ('time_to_examine', 'time_to_deep_exam', 'required_key_item'),
        }),
    )


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display  = ('name', 'case', 'place', 'person', 'evidence_value', 'require_deep_search')
    list_filter   = ('case', 'require_deep_search')
    search_fields = ('name', 'description', 'deep_description')
    raw_id_fields = ('case', 'place', 'person')
    fieldsets = (
        (None, {
            'fields': ('name', 'case', 'image_url'),
        }),
        ('Beskrivning', {
            'fields': ('description', 'deep_description'),
        }),
        ('Bevis & Tid', {
            'fields': ('evidence_value', 'time_to_examine', 'time_to_deep_exam', 'require_deep_search'),
            'description': 'Värde och tidsåtgång vid undersökning.',
        }),
    )


@admin.register(Dialog)
class DialogAdmin(admin.ModelAdmin):
    list_display = (
        'node_key',
        'case',
        'person',
        'is_entry_node',
        'emotion_above',
        'emotion_below',
        'visit_count',
        'is_evidence',
    )
    list_filter = (
        'case',
        'person',
        'is_entry_node',
        'is_evidence',
    )
    search_fields = (
        'node_key',
        'text',
        'reaction_description',
    )
    raw_id_fields = (
        'case',
        'person',
        'hint_person',
        'evidence_item',
    )
    ordering = ('case', 'person', 'node_key')
    fieldsets = (
        (None, {
            'fields': (
                'case',
                'person',
                'node_key',
                'text',
                'reaction_description',
            ),
        }),
        ('Tillgänglighet', {
            'fields': (
                'is_entry_node',
                'requires_visits',
                'visit_count',
            ),
            'description': 'Styr när den här dialogen blir tillgänglig för spelaren.',
        }),
        ('Känslor & Bevis', {
            'fields': (
                'emotion_above',
                'emotion_below',
                'is_evidence',
                'hint_person',
                'evidence_item',
                'time_for_option',
            ),
            'description': 'Inställningar som påverkar karaktärens reaktion och bevisflaggning.',
        }),
    )


@admin.register(DialogOption)
class DialogOptionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'dialog', 'short_text', 'attitude_above', 'attitude_below', 'attitude_change',
        'item', 'person', 'place', 'next_dialog'
    )
    list_filter = (
        'dialog__case', 'dialog__person', 'item', 'person', 'place'
    )
    search_fields = (
        'option_text',
    )
    raw_id_fields = (
        'dialog', 'item', 'person', 'place', 'next_dialog'
    )

    def short_text(self, obj):
        return obj.option_text[:50]
        short_text.short_description = 'Option Text (first 50 chars)'