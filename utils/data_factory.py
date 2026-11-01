import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class Employee:
    first_name: str
    middle_name: str
    last_name: str

    @property
    def full_name(self) -> str:
        return " ".join(
            part for part in (self.first_name, self.middle_name, self.last_name) if part
        )


def new_employee() -> Employee:
    """生成唯一员工数据，避免共享演示环境中的数据冲突。"""
    suffix = uuid.uuid4().hex[:8]
    return Employee(
        first_name="AutoTest",
        middle_name="Qa",
        last_name=f"User{suffix}",
    )
