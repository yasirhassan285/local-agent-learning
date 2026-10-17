from ollama import chat
from pydantic import BaseModel


class PackageInfo(BaseModel):
    package: str
    version: str


response = chat(
    model="qwen3:8b",
    messages=[
        {
            "role": "user",
            "content": (
                "Extract the package name and version from: "
                "ollama==0.6.0"
            ),
        }
    ],
    format=PackageInfo.model_json_schema(),
)


package_info = PackageInfo.model_validate_json(
    response.message.content
)

print(package_info)
print(package_info.package)
print(package_info.version)