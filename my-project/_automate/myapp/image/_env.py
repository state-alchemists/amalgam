from zrb import Env

image_env = Env(
    name="IMAGE",
    os_name="CONTAINER_MYAPP_IMAGE",
    default="{{input.myapp_image}}",
)
