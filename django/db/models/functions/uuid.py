from django.db import NotSupportedError
from django.db.models.expressions import Func
from django.db.models.fields import UUIDField


class UUID4(Func):
    output_field = UUIDField()

    def as_sql(self, compiler, connection, **extra_context):
        raise NotSupportedError("UUID4 is not supported on this database backend.")

    def as_postgres(self, compiler, connection, **extra_context):
        if connection.features.is_postgresql_18:
            function = "UUIDV4"
        else:
            function = "GEN_RANDOM_UUID"
        super().as_sql(compiler, connection, function=function, **extra_context)

    def as_mysql(self, compiler, connection, **extra_context):
        if connection.features.supports_uuid4_function:
            function = "UUID_V4"
        elif connection.mysql_is_mariadb:
            raise NotSupportedError("UUID4 requires MariaDB version 11.7 or later.")
        else:
            raise NotSupportedError("UUID4 is not supported on MySQL.")
        super().as_sql(compiler, connection, function=function, **extra_context)

    def as_oracle(self, compiler, connection, **extra_context):
        if connection.features.supports_uuid4_function:
            function = "UUID"
        else:
            raise NotSupportedError("UUID4 requires Oracle version 23ai or later.")
        super().as_sql(compiler, connection, function=function, **extra_context)


class UUID7(Func):
    output_field = UUIDField()

    def as_sql(self, compiler, connection, **extra_context):
        raise NotSupportedError("UUID7 is not supported on this database backend.")

    def as_postgres(self, compiler, connection, **extra_context):
        if connection.features.supports_uuid7_function:
            function = "UUIDV7"
        else:
            raise NotSupportedError("UUID7 requires PostgreSQL version 18 or later.")
        super().as_sql(compiler, connection, function=function, **extra_context)

    def as_mysql(self, compiler, connection, **extra_context):
        if connection.features.supports_uuid7_function:
            function = "UUID_V7"
        elif connection.mysql_is_mariadb:
            raise NotSupportedError("UUID7 requires MariaDB version 11.7 or later.")
        else:
            raise NotSupportedError("UUID7 is not supported on MySQL.")
        super().as_sql(compiler, connection, function=function, **extra_context)
