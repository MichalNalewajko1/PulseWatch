from datetime import datetime
from typing import Self, Annotated

from pydantic import (BaseModel, Field, AfterValidator, model_validator)

def validate_timestamp_format(
    value: str
) -> str:
    try:
        datetime.strptime(
            value,
            "%Y-%m-%d %H:%M:%S"
        )
    except ValueError as error:
        raise ValueError(
            "timestamp musi mieć format "
            "YYYY-MM-DD HH:MM:SS"
        ) from error

    return value

TimestampString = Annotated[str, Field(min_length=1), AfterValidator(validate_timestamp_format)]


class MemoryMetrics(BaseModel):
    total_bytes: int = Field(ge=0)
    available_bytes: int = Field(ge=0)
    used_bytes: int = Field(ge=0)
    usage_percent: float = Field(ge=0, le=100)

    @model_validator(mode="after")
    def validate_byte_values(self) -> Self:
        calculated_total = (
            self.available_bytes
            + self.used_bytes
        )

        if calculated_total != self.total_bytes:
            raise ValueError(
                "available_bytes + used_bytes "
                "musi być równe total_bytes"
            )
            

        return self


class DiskMetrics(BaseModel):
    total_bytes: int = Field(ge=0)
    free_bytes: int = Field(ge=0)
    used_bytes: int = Field(ge=0)
    usage_percent: float = Field(ge=0, le=100)

    @model_validator(mode="after")
    def validate_byte_values(self) -> Self:
        calculated_total = (
            self.free_bytes
            + self.used_bytes
        )

        if calculated_total != self.total_bytes:
            raise ValueError(
                "free_bytes + used_bytes "
                "musi być równe total_bytes"
            )

        return self


class SystemSnapshotPayload(BaseModel):
    timestamp: TimestampString
    computer_name: str = Field(
        min_length=1,
        max_length=255
    )
    cpu_usage_percent: float = Field(
        ge=0,
        le=100
    )
    memory: MemoryMetrics
    disk: DiskMetrics


class SnapshotCreatedResponse(BaseModel):
    status: str
    id: int = Field(gt=0)
    computer_name: str
    timestamp: TimestampString


class SnapshotResponse(BaseModel):
    id: int = Field(gt=0)

    timestamp: TimestampString
    computer_name: str = Field(
        min_length=1,
        max_length=255
    )

    cpu_usage_percent: float = Field(
        ge=0,
        le=100
    )

    memory_total_bytes: int = Field(ge=0)
    memory_available_bytes: int = Field(ge=0)
    memory_used_bytes: int = Field(ge=0)

    memory_usage_percent: float = Field(
        ge=0,
        le=100
    )

    disk_total_bytes: int = Field(ge=0)
    disk_free_bytes: int = Field(ge=0)
    disk_used_bytes: int = Field(ge=0)

    disk_usage_percent: float = Field(
        ge=0,
        le=100
    )