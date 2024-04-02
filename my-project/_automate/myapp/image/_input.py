from zrb import StrInput

image_input = StrInput(
    name="myapp-image",
    description='Image name of "myapp"',
    prompt='Image name of "myapp"',
    default="docker.io/gofrendi/myapp:latest",
)
