import flet as ft

#default UI settings

text_color = "green"
button_color = "yellow"
font = "TimesNewRoman"

example_task_list = [
    {
        "id": 1,
        "short_name": "Wash"
    },
    {
        "id": 2,
        "short_name": "Clean"
    }
]

example_task = {
    "id": 1,
    "short_name": "Wash",
    "explain": "Wash your hands!",
    "creation_date": "12.11.2024",
    "deadline": "9.12.2024"
}


def main(page: ft.Page):
    page.title = "Task list"


    class MyButton(ft.ElevatedButton):
        def __init__(self, text, func):
            super().__init__()
            self.text = text
            self.color = text_color
            self.bgcolor = button_color
            self.on_click = func


    class MyText(ft.Text):
        def __init__(self, text):
            super().__init__()
            self.value = text
            self.color = text_color
            self.font_family = font


        def chg_text_color(self):
            self.color = text_color

        def chg_font(self):
            self.font_family = font


    class MyTextField(ft.TextField):
        def __init__(self, text, max_length=100, width=200):
            super().__init__()
            self.color = text_color
            self.hint_text = text
            self.max_length = max_length
            self.width = width

        def chg_text_color(self):
            self.color = text_color


    class AddTask(ft.Column):
        def __init__(self):
            super().__init__()
            self.short_name = MyTextField("Short name of the Task", 30)
            self.explain = MyTextField("Explanation of the Task", 200, 400)
            self.deadline = MyTextField("Deadline of the Task", 10)
            self.add_button = MyButton("Add the Task", self.add_task)

            self.controls = [
                self.short_name,
                self.explain,
                self.deadline,
                self.add_button
            ]
            self.spacing = 30
            self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        def add_task(self, e):
            page.go("/")


    class Settings(ft.Column):
        def __init__(self):
            super().__init__()

            self.text_color = ft.Dropdown("green", options=[
                    ft.dropdown.Option("green"),
                    ft.dropdown.Option("white"),
                    ft.dropdown.Option("gray")
            ], width=200, on_change=self.chg_text_color)

            self.button_color = ft.Dropdown("yellow", options=[
                    ft.dropdown.Option("yellow"),
                    ft.dropdown.Option("green"),
                    ft.dropdown.Option("gray")
            ], width=200, on_change=self.chg_button_color)

            self.font = ft.Dropdown("TimesNewRoman", options=[
                    ft.dropdown.Option("TimesNewRoman")
            ], width=200, on_change=self.chg_font)

            self.controls = [
                MyText("Text color"),
                self.text_color,
                MyText("Button color"),
                self.button_color,
                MyText("Font"),
                self.font,
                MyButton("Done", self.done),
                MyButton("Generate Database", None)
            ]

            self.spacing = 30
            self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        def chg_text_color(self, e):
            global text_color
            text_color = self.text_color.value

        def chg_button_color(self, e):
            global button_color
            button_color = self.button_color.value

        def chg_font(self, e):
            global font
            font = self.font.value

        def done(self, e):
            Vaddtask.controls[1] = AddTask()
            Vwelcome.controls[1] = Welcome()
            Vsettings.controls[1] = Settings()
            page.go("/")


    class Welcome(ft.Column):
        def __init__(self):
            super().__init__()

            self.controls = [
                MyButton("Show tasks", lambda _: page.go("/tasks")),
                MyButton("Add task", lambda _: page.go("/addtask")),
                MyButton("Cat?", None),
                MyText("Current tasks: "),
                MyText("Solved tasks: "),
                MyText("Failed tasks: ")
            ]

            self.spacing = 20
            self.height = 160
            self.wrap = True
            self.width = 300
            self.alignment = ft.MainAxisAlignment.CENTER


    class ChooseTask(ft.Row):
        def __init__(self, id, short_name):
            super().__init__()
            self.id = id
            self.short_name = short_name
            self.vertical_alignment = ft.CrossAxisAlignment.CENTER

            self.controls = [
                MyText(f"{id}.  "),
                MyButton(self.short_name, self.more_information)
            ]

        def more_information(self, e):
            Vtask.controls[0] = ft.AppBar(title=MyText(self.short_name), bgcolor=ft.Colors.CYAN_700)
            Vtask.controls[1] = ShowTask(self.id)
            page.go("/tasks/task")


    class ListOfTasks(ft.Column):
        def __init__(self):
            super().__init__()

            self.gain_tasks = example_task_list

            self.controls = [ChooseTask(task["id"], task["short_name"]) for task in self.gain_tasks]


    class ShowTask(ft.Column):
        def __init__(self, id):
            super().__init__()
            self.id = id
            self.gain_task = example_task

            self.controls = [
                MyText(self.gain_task["explain"]),
                MyText(self.gain_task["creation_date"]),
                MyText(self.gain_task["deadline"]),
                MyButton("Done", self.complete_task)
            ]

        def complete_task(self, e):
            Vtasks.controls[1] = ListOfTasks()
            page.go("/tasks")


    Vwelcome = ft.View(
        "/",
        [
            ft.AppBar(title=MyText("Welcome to the Task list!"), bgcolor=ft.Colors.CYAN_700, actions=[
                ft.IconButton(ft.Icons.SETTINGS, on_click=lambda _: page.go("/settings"))
            ]),
            Welcome()
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )


    Vsettings = ft.View(
        "/settings",
        [
            ft.AppBar(title=MyText("Settings"), bgcolor=ft.Colors.CYAN_700),
            Settings()
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    Vtasks = ft.View(
        "/tasks",
        [
            ft.AppBar(title=MyText("List of Tasks"), bgcolor=ft.Colors.CYAN_700),
            MyText("Hello)")
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    Vtask = ft.View(
        "/tasks/task",
        [
            MyText("Hello)"),
            MyText("Hello)")
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    Vaddtask = ft.View(
        "/addtask",
        [
            ft.AppBar(title=MyText("Add task"), bgcolor=ft.Colors.CYAN_700),
            AddTask()
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    def route_change(route):
        page.views.clear()
        page.views.append(Vwelcome)

        if page.route == "/tasks":
            Vtasks.controls[1] = ListOfTasks()
            page.views.append(Vtasks)

        if page.route == "/tasks/task":
            page.views.append(Vtask)

        if page.route == "/addtask":
            page.views.append(Vaddtask)

        if page.route == "/settings":
            page.views.append(Vsettings)

        page.update()


    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(main, view=ft.AppView.WEB_BROWSER)