from enum import Enum


class SlashCommands(str, Enum):
    """Слэш команды бота."""

    START = "start"
    HELP = "help"
    SETTINGS = "settings"
    MENU = "menu"
    LESSONS = "lessons"
    CAFE = "cafe"
    LAUNDRY = "laundry"
    ELECTIVES = "electives"
    EDUCATORS = "educators"
    CANCEL = "cancel"
    STOP = "stop"


class TextCommands(str, Enum):
    """Текстовые команды бота."""

    START = "Старт"
    HELP = "Помощь"
    SETTINGS = "⚙️Настройки"
    MENU = "Меню"
    LESSONS = "📓Уроки"
    CAFE = "🍴Меню"
    LAUNDRY = "💦Прачечная"
    ELECTIVES = "📖Элективы"
    EDUCATORS = "👩‍✈️Воспитатели"
    ADMIN_PANEL = "❗Админ панель"
    CANCEL = "Отмена"
    STOP = CANCEL


class NotifyTypes(str, Enum):
    """Типы уведомлений для пользователей."""

    ALL = "all"
    GRADE = "grade"
    CLASS = "class"
    GRADE_10 = "grade_10"
    GRADE_11 = "grade_11"


class UserCallback(str, Enum):
    """Callback дата, которую используют все пользователей."""

    MAIN_MENU = "main_menu"
    SETTINGS = "settings"
    LAUNDRY = "laundry"
    EDUCATORS = "educators"
    ELECTIVES = "electives"
    CAFE_MENU = "cafe_menu"
    LESSONS = "open_lessons_on_"

    START = "start"
    SWITCH = "switch"
    EDIT = "edit"
    CANCEL = "cancel"

    WASHING = "washing"
    DRYING = "drying"
    EMPTY = "empty"

    CHANGE_GRADE = "change_grade"
    LESSONS_NOTIFY = "lessons_notify"
    NEWS_NOTIFY = "news_notify"


class AdminCallback(str, Enum):
    """Callback дата, которую используют админы."""

    OPEN_ADMIN_PANEL = "open_admin_panel"

    AUTO_UPDATE_CAFE_MENU = "auto_update_cafe_menu"
    EDIT_CAFE_MENU = "edit_cafe_menu"
    EDIT_BREAKFAST = "edit_breakfast"
    EDIT_LUNCH = "edit_lunch"
    EDIT_DINNER = "edit_dinner"
    EDIT_SNACK = "edit_snack"
    EDIT_SUPPER = "edit_supper"
    EDIT_EDUCATORS = "edit_educators"

    UPLOAD_LESSONS = "upload_lessons_"
    UPLOAD_LESSONS_FOR_10 = UPLOAD_LESSONS + "for_10"
    UPLOAD_LESSONS_FOR_11 = UPLOAD_LESSONS + "for_11"

    DO_A_NOTIFY_FOR_ = "do_a_notify_for_"
    NOTIFY_FOR_ALL = DO_A_NOTIFY_FOR_ + NotifyTypes.ALL
    NOTIFY_FOR_GRADE = DO_A_NOTIFY_FOR_ + NotifyTypes.GRADE
    NOTIFY_FOR_CLASS = DO_A_NOTIFY_FOR_ + NotifyTypes.CLASS

    OPEN_ADMINS_LIST_PAGE_ = "open_admins_list_page_"
    CHECK_ADMIN_ = "check_admin_"
    REMOVE_ADMIN_ = "remove_admin_"
    REMOVE_ADMIN_SURE_ = REMOVE_ADMIN_ + "sure_"
    ADD_NEW_ADMIN = "add_new_admin"
    ADD_NEW_ADMIN_SURE = "add_new_admin_sure"

    CONFIRM = "confirm_in_state"
    NOT_CONFIRM = "not_confirm_in_state"


class Roles(str, Enum):
    """Роли (права доступа) пользователей."""

    SUPERADMIN = "superadmin"
    ADMIN = "admin"
