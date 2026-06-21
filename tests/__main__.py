import time
import asyncio

from gigachat_controller import GigaChatController

config = {
    "credentials": "MDE5ZTAzY2ItMjdlZC03OTgxLTg3ZTctNmY0ZDBiYWZlYTkwOmRlMjcxNzZkLTNkMDEtNDA3MS05OWY4LTcxNzE3MTE2MjA1NQ==",
    "ca_bundle_file": "C:\\Users\\Isui\\Downloads\\russian_trusted_root_ca.cer",
    "model": "GigaChat-2",
}

gcc = GigaChatController(config=config)
print(gcc.info())

models = gcc.models()
for model in models.data:
    print(model.id_)

response = gcc.invoke("Привет. Назови столицу России.")
print(response)

async def test_async():
    response = await asyncio.gather(
        gcc.ainvoke("Привет. Назови столицу Конго."),
        gcc.ainvoke("Привет. Назови столицу Кот-Дивуара.")
    )
    print(response)

asyncio.run(test_async())
