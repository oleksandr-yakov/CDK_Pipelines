from aws_cdk import cdk
import aws_cdk.aws_dynamodb as dynamodb


class DataDeletionStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Отримуємо посилання на існуючі таблиці DynamoDB
        card_table = dynamodb.Table.from_table_name(self, "CardTable", "CardTable-dev")
        list_table = dynamodb.Table.from_table_name(self, "ListTable", "ListTable-dev")

        # Функція для видалення даних з таблиці
        def delete_data(table):
            table.grant_full_access(self)  # Додайте необхідні дозволи
            table.scan().foreach_page(delete_item)

        def delete_item(items, _):
            for item in items:
                item.delete()

        # Видаляємо дані з таблиць
        delete_data(card_table)
        delete_data(list_table)


app = cdk.App()
DataDeletionStack(app, "DataDeletionStack")
app.synth()
