import bpy
import requests

# register
def user_register(username,  email, password):
    url = "https://tintype-backend.vercel.app/api/auth/register"
    data = {"username": username, "email": email, "password": password}
    response = requests.post(url, data=data)
    return response.json()

# login
def user_login(username, password):
    url = "https://tintype-backend.vercel.app/api/auth/login"
    data = {"username": username, "password": password}
    response = requests.post(url, data=data)
    return response.json()

# send messsage
def send_message(_from, to, message):
    url = "https://tintype-backend.vercel.app/api/message/addmsg"
    data = {"from": _from, "to": to, "message": message}
    response = requests.post(url, data=data)
    return response.json()

# get messages
def get_messages(_from, to):
    url = "https://tintype-backend.vercel.app/api/message/getmsg"
    data = {"from": _from, "to": to}
    response = requests.post(url, data=data)
    return response.json()

class chat_panel(bpy.types.Panel):
    bl_idname = "CHAT_PT_panel"
    bl_label = "Chats panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tintype"
    bl_icon = "MESH_CUBE"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "chat_message")
        layout.operator("addon.get_messages")
        layout.operator("addon.send_message")

class auth_panel(bpy.types.Panel):
    bl_idname = "AUTH_PT_panel"
    bl_label = "Auth panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tintype"
    bl_icon = "MESH_CUBE"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "auth_username")
        layout.prop(context.scene, "auth_email")
        layout.prop(context.scene, "auth_password")
        layout.operator("addon.user_register")
        layout.operator("addon.user_login")


class RegisterUserOperator(bpy.types.Operator):
    bl_idname = "addon.user_register"
    bl_label = "Register"

    def execute(self, context):
        username = context.scene.auth_username
        email = context.scene.auth_email
        password = context.scene.auth_password
        response = user_register(username, email, password)
        if response.get("error"):
            self.report({"ERROR"}, response.get("error"))
        else:
            self.report({"INFO"}, "User registered successfully!")
        return {'FINISHED'}

class LoginUserOperator(bpy.types.Operator):
    bl_idname = "addon.user_login"
    bl_label = "Login"

    def execute(self, context):
        username = context.scene.auth_username
        password = context.scene.auth_password
        response = user_login(username, password)
        if response.get("error"):
            self.report({"ERROR"}, response.get("error"))
        else:
            self.report({"INFO"}, "User Logged in")
        return {"FINISHED"}

class SendMessageOperator(bpy.types.Operator):
    bl_idname = "addon.send_message"
    bl_label = "Send"

    def execute(self, context):
        message = context.scene.chat_message
        response = send_message(
            "6432fa28e763408199b9f124", "6432fa48e763408199b9f128", message)
        if response.get("error"):
            self.report({"ERROR"}, response.get("error"))
        else:
            self.report({"INFO"}, "Message Sent")
        return {"FINISHED"}


def register():
    bpy.types.Scene.auth_username = bpy.props.StringProperty(name="Username")
    bpy.types.Scene.auth_email = bpy.props.StringProperty(name="Email")
    bpy.types.Scene.auth_password = bpy.props.StringProperty(name="Password")
    bpy.types.Scene.chat_message = bpy.props.StringProperty(name="Messages")

    bpy.utils.register_class(auth_panel)
    bpy.utils.register_class(chat_panel)

    bpy.utils.register_class(RegisterUserOperator)
    bpy.utils.register_class(LoginUserOperator)
    bpy.utils.register_class(SendMessageOperator)


def unregister():
    bpy.utils.unregister_class(auth_panel)
    bpy.utils.unregister_class(chat_panel)

    bpy.utils.unregister_class(RegisterUserOperator)
    bpy.utils.unregister_class(LoginUserOperator)
    bpy.utils.unregister_class(SendMessageOperator)

    del bpy.types.Scene.chat_message
    del bpy.types.Scene.auth_username
    del bpy.types.Scene.auth_email
    del bpy.types.Scene.auth_password


if __name__ == "__main__":
    register()
