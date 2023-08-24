FILE_FORMAT = r"([^,]+),([^,]+),([^,]+),([^,]+),([^,]+),([^,]+)"
CONTACT_OUTPUT_FORMAT = (
    "{last_name},"
    "{first_name},"
    "{middle_name},"
    "{organization},"
    "{work_phone},"
    "{personal_phone}"
)
FIELDS = [
    "Фамилия",
    "Имя",
    "Отчество",
    "Организация",
    "Телефон рабочий",
    "Телефон личный",
]
CLASS_FIELDS = [
    "last_name",
    "first_name",
    "middle_name",
    "organization",
    "work_phone",
    "personal_phone",
]
MENU_OPTIONS = {
    1: "Вывод постранично записей из справочника на экран",
    2: "Добавление новой записи в справочник",
    3: "Редактирование записи в справочнике",
    4: "Удаление записи из справочника",
    5: "Поиск записей по характеристикам",
    6: "Выход",
}
SEARCH_THRESHOLD = 70
