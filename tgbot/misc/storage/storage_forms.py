from typing import Optional

from tgbot.misc.forms.form import Form
from tgbot.misc.storage.storage_common import StorageCommon


class StorageForms:

    @staticmethod
    async def all(global_data: dict = None) -> dict[str, Form]:
        global_data = await StorageCommon.get_data(global_data)
        return global_data.get("forms", {})

    @staticmethod
    async def set_all(forms: dict[str, Form], global_data: dict = None):
        global_data = await StorageCommon.get_data(global_data)
        global_data["forms"] = forms

    @staticmethod
    async def get(uuid: str) -> Optional[dict]:
        forms = await StorageForms.all()
        return forms.get(uuid, None)

    @staticmethod
    async def set(form: Form, global_data: dict = None):
        global_data = await StorageCommon.get_data(global_data)
        forms = await StorageForms.all(global_data)
        forms[form.uuid] = form
        await StorageForms.set_all(forms, global_data)
        await StorageCommon.save(global_data)
