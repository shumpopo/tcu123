import json
import re
from urllib.request import urlopen
import pyttsx3
import speech_recognition as sr
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import Snackbar
import Love_responses as Love
import Academic_responses as Academic
import Family_responses as Family
# ----------------------------------------------------------------------------------------------------------------------

Window.size = (325, 670)

# ----------------------------------------------------------------------------------------------------------------------
engine = pyttsx3.init()


# ----------------------------------------------------------------------------------------------------------------------

class Command(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name = "fonts/PoppinsEL.otf"
    font_size = 14


def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculates the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def check_all_messages_love(message):
    highest_prob_list = {}

    def love_response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    love_response(Love.love(), ['i', 'want', 'to', 'confess'], required_words=['want', 'confess'])
    love_response(Love.love(), ['i', 'want', 'to', 'confess'], required_words=['confess'])
    love_response(Love.love(), ['i', 'want', 'to', 'confess'], required_words=['want'])

    love_response(Love.broken(), ['im', 'getting', 'bored', 'of', 'my', 'partner', 'what', 'should', 'i', 'do'],
                  required_words=['bored', 'partner'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)

    return Love.unknown() if highest_prob_list[best_match] < 1 else best_match


def check_all_messages_academic(message):
    highest_prob_list = {}

    def academic_response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    academic_response(Academic.academic(), ['i', 'want', 'to', 'go'], required_words=['want', 'go'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)

    return Academic.unknown() if highest_prob_list[best_match] < 1 else best_match


def check_all_messages_family(message):
    highest_prob_list = {}

    def family_response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    family_response(Family.family(), ['i', 'want', 'to', 'go'], required_words=['want', 'go'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)

    return Family.unknown() if highest_prob_list[best_match] < 1 else best_match

# Used to get the response
def love_get_response(love_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', love_input.lower())
    response = check_all_messages_love(split_message)
    return response


def Academic_get_response(academic_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', academic_input.lower())
    response = check_all_messages_academic(split_message)
    return response


def family_get_response(family_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', family_input.lower())
    response = check_all_messages_academic(split_message)
    return response




class Response(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name = "fonts/PoppinsEL.otf"
    font_size = 14


class User_data(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name = "fonts/PoppinsEL.otf"
    font_size = 13


class TCUAdvisor(MDApp):
    def build(self):

        global screen
        screen = ScreenManager(transition=SlideTransition(duration=.8))
        screen.add_widget(Builder.load_file("Introduction.kv"))
        screen.add_widget(Builder.load_file("Introduction1.kv"))
        screen.add_widget(Builder.load_file("Login.kv"))
        screen.add_widget(Builder.load_file("Register.kv"))
        screen.add_widget(Builder.load_file("Admin_login.kv"))
        screen.add_widget(Builder.load_file("Admin_Home-screen.kv"))
        screen.add_widget(Builder.load_file("Welcome-screen.kv"))
        screen.add_widget(Builder.load_file("Home-screen.kv"))
        screen.add_widget(Builder.load_file("Notification-screen.kv"))
        screen.add_widget(Builder.load_file("Profile-screen.kv"))
        screen.add_widget(Builder.load_file("About.kv"))
        screen.add_widget(Builder.load_file("Love_message-screen.kv"))
        screen.add_widget(Builder.load_file("Academic_message-screen.kv"))
        screen.add_widget(Builder.load_file("Family_message-screen.kv"))

        return screen

    # AI Voices----------------------------------------------------------------------------------------------------------
    def speak_male(self, text):
        engine.setProperty('rate', 160)
        engine.setProperty('pitch', 100)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)

        engine.say(text)
        engine.runAndWait()

    def speak_female(self, text):
        engine.setProperty('rate', 160)
        engine.setProperty('pitch', 100)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)

        engine.say(text)
        engine.runAndWait()

    # Command & Responses -----------------------------------------------------------------------------------

    def send_love(self):
        global size, halign, command
        if screen.get_screen('Love_message-screen').text_input != "":
            love_input = screen.get_screen('Love_message-screen').text_input.text
            if len(love_input) < 6:
                size = .22
                halign = "center"
            elif len(love_input) < 11:
                size = .32
                halign = "center"
            elif len(love_input) < 16:
                size = .45
                halign = "center"
            elif len(love_input) < 21:
                size = .58
                halign = "center"
            elif len(love_input) < 26:
                size = .71
                halign = "center"
            else:
                size = .77
                halign = "left"

            screen.get_screen('Love_message-screen').chat_list.add_widget(
                Command(text=love_input, size_hint_x=size, halign=halign))

            screen.get_screen('Love_message-screen').chat_list.add_widget(
                Response(text=love_get_response(love_input), size_hint_x=size, halign=halign))

            screen.get_screen('Love_message-screen').text_input.text = ""

    def send_academic(self):
        global size, halign, command
        if screen.get_screen('Academic_message-screen').text_input != "":
            academic_input = screen.get_screen('Academic_message-screen').text_input.text
            if len(academic_input) < 6:
                size = .22
                halign = "center"
            elif len(academic_input) < 11:
                size = .32
                halign = "center"
            elif len(academic_input) < 16:
                size = .45
                halign = "center"
            elif len(academic_input) < 21:
                size = .58
                halign = "center"
            elif len(academic_input) < 26:
                size = .71
                halign = "center"
            else:
                size = .77
                halign = "left"

            screen.get_screen('Academic_message-screen').chat_list.add_widget(
                Command(text=academic_input, size_hint_x=size, halign=halign))

            screen.get_screen('Academic_message-screen').chat_list.add_widget(
                Response(text=Academic_get_response(academic_input), size_hint_x=size, halign=halign))

            screen.get_screen('Academic_message-screen').text_input.text = ""

    def send_family(self):
        global size, halign, command
        if screen.get_screen('Family_message-screen').text_input != "":
            user_input = screen.get_screen('Family_message-screen').text_input.text
            if len(user_input) < 6:
                size = .22
                halign = "center"
            elif len(user_input) < 11:
                size = .32
                halign = "center"
            elif len(user_input) < 16:
                size = .45
                halign = "center"
            elif len(user_input) < 21:
                size = .58
                halign = "center"
            elif len(user_input) < 26:
                size = .71
                halign = "center"
            else:
                size = .77
                halign = "left"

            screen.get_screen('Family_message-screen').chat_list.add_widget(
                Command(text=user_input, size_hint_x=size, halign=halign))

            screen.get_screen('Family_message-screen').chat_list.add_widget(
                Response(text=family_get_response(user_input), size_hint_x=size, halign=halign))

            screen.get_screen('Family_message-screen').text_input.text = ""

    def Love_take_command(self):

        global size, halign, command

        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Listening . . .")
            r.pause_threshold = 1
            text = r.listen(source)
        try:
            print("Recognizing. . .")
            command = r.recognize_google(text, language='en-in')
            if len(command) < 6:
                size = .22
                halign = "center"
            elif len(command) < 11:
                size = .32
                halign = "center"
            elif len(command) < 16:
                size = .45
                halign = "center"
            elif len(command) < 21:
                size = .58
                halign = "center"
            elif len(command) < 26:
                size = .71
                halign = "center"
            else:
                size = .77
                halign = "left"
            screen.get_screen('Love_message-screen').chat_list.add_widget(
                Command(text=command, size_hint_x=size, halign=halign))

            screen.get_screen('Love_message-screen').chat_list.add_widget(
                Response(text=love_get_response(command), size_hint_x=size, halign=halign))

            self.speak_female(love_get_response(command))

            return

        except Exception as e:
            print(e)

            return "None"

    def Academic_take_command(self):

        global size, halign, command

        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Listening . . .")
            r.pause_threshold = 1
            text = r.listen(source)
        try:
            print("Recognizing. . .")
            command = r.recognize_google(text, language='en-in')
            if len(command) < 6:
                size = .22
                halign = "center"
            elif len(command) < 11:
                size = .32
                halign = "center"
            elif len(command) < 16:
                size = .45
                halign = "center"
            elif len(command) < 21:
                size = .58
                halign = "center"
            elif len(command) < 26:
                size = .71
                halign = "center"
            else:
                size = .77
                halign = "left"
            screen.get_screen('Academic_message-screen').chat_list.add_widget(
                Command(text=command, size_hint_x=size, halign=halign))
            screen.get_screen('Academic_message-screen').text_input.text = ""
            return
        except Exception as e:
            print(e)
            return "None"

    def Family_take_command(self):

        global size, halign, command

        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening . . .")
            r.pause_threshold = 1
            text = r.listen(source)
        try:
            print("Recognizing. . .")
            command = r.recognize_google(text, language='en-in')
            if len(command) < 6:
                size = .22
                halign = "center"
            elif len(command) < 11:
                size = .32
                halign = "center"
            elif len(command) < 16:
                size = .45
                halign = "center"
            elif len(command) < 21:
                size = .58
                halign = "center"
            elif len(command) < 26:
                size = .71
                halign = "center"
            else:
                size = .77
                halign = "left"
            screen.get_screen('Family_message-screen').chat_list.add_widget(
                Command(text=command, size_hint_x=size, halign=halign))
            screen.get_screen('Family_message-screen').text_input.text = ""
            return
        except Exception as e:
            print(e)
            return "None"

    # User Registration----------------------------------------------------------------------------------------------------

    def register(self, name, stud_id, yr_course, section, email, password):

        with open('User_data.json', 'r') as f:
            users = json.loads(f.read())

        for user in users.get('user', []):
            if user.get('Student ID') == stud_id:
                Snackbar(text="Student ID already Existed!",
                         snackbar_animation_dir="Top",
                         font_size='12sp',
                         snackbar_x=.1,
                         size_hint_x=.999,
                         size_hint_y=.07,
                         bg_color=(1, 0, 0, 1),
                         ).open()
                return

        if any(field == "" for field in [name, stud_id, yr_course, section, email, password]):
            Snackbar(text="Please fill out all fields!",
                     snackbar_animation_dir="Top",
                     font_size='12sp',
                     snackbar_x=.1,
                     size_hint_x=.999,
                     size_hint_y=.07,
                     bg_color=(1, 0, 0, 1),
                     ).open()
            return
        else:
            filename = 'User_data.json'
            mydict = {
                "Student ID": stud_id,
                "Name": name,
                "Year & Course": yr_course,
                "Section": section,
                "Email": email,
                "Password": password
            }

            try:
                with open(filename, "r") as f:
                    data = json.load(f)

            except FileNotFoundError:
                data = []

            data["user"].append(mydict)

            with open(filename, "w") as f:
                json.dump(data, f, indent=4)

                Snackbar(text="Registered Successfully!",
                         snackbar_animation_dir="Top",
                         font_size='12sp',
                         snackbar_x=.1,
                         size_hint_x=.999,
                         size_hint_y=.07,
                         bg_color="#537188"
                         ).open()

                self.clear_registration_fields()
                self.root.current = 'Login'
                return

    # Admin & User Login----------------------------------------------------------------------------------------------------
    def user_login(self, stud_id, password):
        if not stud_id:
            Snackbar(text="Please Enter your ID!",
                     snackbar_animation_dir="Top",
                     font_size='12sp',
                     snackbar_x=.1,
                     size_hint_x=.999,
                     size_hint_y=.07,
                     bg_color=(1, 0, 0, 1),
                     ).open()
            return
        if not password:
            Snackbar(text="Please Enter your Password!",
                     snackbar_animation_dir="Top",
                     font_size='12sp',
                     snackbar_x=.1,
                     size_hint_x=.999,
                     size_hint_y=.07,
                     bg_color=(1, 0, 0, 1),
                     ).open()
            return

        with open('User_data.json', 'r') as f:
            users = json.loads(f.read())

        for user in users.get('user', []):
            if user.get('Student ID') == stud_id:
                if user.get('Password') == password:
                    self.root.current = 'Welcome-screen'
                    self.clear_user_login_fields()

                    name = user.get('Name', '')
                    screen.get_screen('Profile-screen').add_widget(
                        User_data(text=name, font_name="fonts/OpenSans-Semibold.ttf",
                                  pos_hint={"center_x": .73, "center_y": .61}))

                    stud_id = user.get('Student ID', '')
                    screen.get_screen('Profile-screen').add_widget(
                        User_data(text=stud_id, font_name="fonts/OpenSans-Semibold.ttf",
                                  pos_hint={"center_x": .73, "center_y": .51}))

                    yr_course = user.get('Year & Course', '')
                    screen.get_screen('Profile-screen').add_widget(
                        User_data(text=yr_course, font_name="fonts/OpenSans-Semibold.ttf",
                                  pos_hint={"center_x": .73, "center_y": .41}))

                    section = user.get('Section', '')
                    screen.get_screen('Profile-screen').add_widget(
                        User_data(text=section, font_name="fonts/OpenSans-Semibold.ttf",
                                  pos_hint={"center_x": .73, "center_y": .31}))

                    email = user.get('Email', '')
                    screen.get_screen('Profile-screen').add_widget(
                        User_data(text=email, font_name="fonts/OpenSans-Semibold.ttf",
                                  pos_hint={"center_x": .73, "center_y": .21}))

                    return

        for user in users.get('user', []):
            if user.get('Student ID') != stud_id:
                if user.get('Password') == password:
                    Snackbar(text="Invalid Student ID & Password!",
                             snackbar_animation_dir="Top",
                             font_size='12sp',
                             snackbar_x=.1,
                             size_hint_x=.999,
                             size_hint_y=.07,
                             bg_color=(1, 0, 0, 1),
                             ).open()
                    return

        for user in users.get('user', []):
            if user.get('Student ID') == stud_id:
                if user.get('Password') != password:
                    Snackbar(text="Invalid Student ID & Password!",
                             snackbar_animation_dir="Top",
                             font_size='12sp',
                             snackbar_x=.1,
                             size_hint_x=.999,
                             size_hint_y=.07,
                             bg_color=(1, 0, 0, 1),
                             ).open()
                    return

        for user in users.get('user', []):
            if user.get('Student ID') != stud_id:
                if user.get('Password') != password:
                    Snackbar(text="Invalid Student ID & Password!",
                             snackbar_animation_dir="Top",
                             font_size='12sp',
                             snackbar_x=.1,
                             size_hint_x=.999,
                             size_hint_y=.07,
                             bg_color=(1, 0, 0, 1),
                             ).open()
                    return

    def admin_login(self, admin_id, admin_password):
        if not admin_id:
            Snackbar(text="Please Enter your Admin ID!",
                     snackbar_animation_dir="Top",
                     font_size='12sp',
                     snackbar_x=.1,
                     size_hint_x=.999,
                     size_hint_y=.07,
                     bg_color=(1, 0, 0, 1),
                     ).open()
            return

        if not admin_password:
            Snackbar(text="Please Enter your Admin Password!",
                     snackbar_animation_dir="Top",
                     font_size='12sp',
                     snackbar_x=.1,
                     size_hint_x=.999,
                     size_hint_y=.07,
                     bg_color=(1, 0, 0, 1),
                     ).open()
            return

        with open('Admin_data.json', 'r') as f:
            ADMIN = json.loads(f.read())

        for admin in ADMIN.get('admin', []):
            if admin.get('Admin ID') == admin_id:
                if admin.get('Admin Password') == admin_password:
                    self.clear_admin_login_fields()
                    self.root.current = 'Adminhome'
                    return

        for admin in ADMIN.get('admin', []):
            if admin.get('Admin ID') != admin_id:
                if admin.get('Admin Password') == admin_password:
                    Snackbar(text="Invalid Admin ID & Admin Password!",
                             snackbar_animation_dir="Top",
                             font_size='12sp',
                             snackbar_x=.1,
                             size_hint_x=.999,
                             size_hint_y=.07,
                             bg_color=(1, 0, 0, 1),
                             ).open()
                    return

        for admin in ADMIN.get('admin', []):
            if admin.get('Admin ID') == admin_id:
                if admin.get('Admin Password') != admin_password:
                    Snackbar(text="Invalid Admin ID & Admin Password!",
                             snackbar_animation_dir="Top",
                             font_size='12sp',
                             snackbar_x=.1,
                             size_hint_x=.999,
                             size_hint_y=.07,
                             bg_color=(1, 0, 0, 1),
                             ).open()
                    return

        for admin in ADMIN.get('admin', []):
            if admin.get('Admin ID') != admin_id:
                if admin.get('Admin Password') != admin_password:
                    Snackbar(text="Invalid Admin ID & Admin Password!",
                             snackbar_animation_dir="Top",
                             font_size='12sp',
                             snackbar_x=.1,
                             size_hint_x=.999,
                             size_hint_y=.07,
                             bg_color=(1, 0, 0, 1),
                             ).open()
                    return

    def forgot_password(self):
        Snackbar(text="Email OTP under maintenance!",
                 snackbar_animation_dir="Top",
                 font_size='12sp',
                 snackbar_x=.1,
                 size_hint_x=.999,
                 size_hint_y=.07,
                 bg_color=(1, 0, 0, 1),
                 ).open()

    # Clearing Inputs-------------------------------------------------------------------------------------------------------

    def clear_admin_fields(self):
        Love = self.root.get_screen('Love_Command-screen')
        Academic = self.root.get_screen('Academic_Command-screen')
        Family = self.root.get_screen('Family_Command-screen')

        Love.ids.command.text = ""
        Love.ids.new_response.text = ""

        Academic.ids.command.text = ""
        Academic.ids.new_response.text = ""

        Family.ids.command.text = ""
        Family.ids.new_response.text = ""

    def clear_registration_fields(self):
        screen = self.root.get_screen('Register')
        screen.ids.name.text = ""
        screen.ids.stud_id.text = ""
        screen.ids.yr_course.text = ""
        screen.ids.section.text = ""
        screen.ids.email.text = ""
        screen.ids.password.text = ""

    def clear_admin_login_fields(self):
        screen = self.root.get_screen('Admin_login')
        screen.ids.admin_id.text = ""
        screen.ids.admin_password.text = ""

    def clear_user_login_fields(self, ):
        screen = self.root.get_screen('Login')
        screen.ids.stud_id.text = ""
        screen.ids.password.text = ""

    # Admin & User Logout---------------------------------------------------------------------------------------------------

    def user_logout(self):
        Snackbar(text="Logged out successful!",
                 snackbar_animation_dir="Top",
                 font_size='12sp',
                 snackbar_x=.1,
                 size_hint_x=.999,
                 size_hint_y=.07,
                 bg_color=(1, 0, 0, 1)
                 ).open()

        self.root.current = 'Login'

    def admin_logout(self):
        Snackbar(text="Logged out successful!",
                 snackbar_animation_dir="Top",
                 font_size='12sp',
                 snackbar_x=.1,
                 size_hint_x=.999,
                 size_hint_y=.07,
                 bg_color=(1, 0, 0, 1)
                 ).open()
        self.root.current = 'Admin_login'

    # Display Users profile & Admin Homescreen users---------------------------------------------------------------------------------------------------------------

    def display_all_user(self):
        with open('User_data.json', 'r') as f:
            users = json.loads(f.read())

        for user in users.get('user', []):
            name = user.get('Name', '')

            screen.get_screen('Adminhome').user_list.add_widget(
                User_data(text="Name:               " + name, font_name="fonts/OpenSans-Bold.ttf",
                          pos_hint={"center_x": .6, "center_y": .5}, font_size=14))

            stud_id = user.get('Student ID', '')
            screen.get_screen('Adminhome').user_list.add_widget(
                User_data(text="Student ID:            " + stud_id, font_name="fonts/OpenSans-Semibold.ttf",
                          pos_hint={"center_x": .6, "center_y": .5}))

            yr_course = user.get('Year & Course', '')
            screen.get_screen('Adminhome').user_list.add_widget(
                User_data(text="Year & Course:          " + yr_course, font_name="fonts/OpenSans-Semibold.ttf",
                          pos_hint={"center_x": .6, "center_y": .5}))

            section = user.get('Section', '')
            screen.get_screen('Adminhome').user_list.add_widget(
                User_data(text="Section:                   " + section, font_name="fonts/OpenSans-Semibold.ttf",
                          pos_hint={"center_x": .6, "center_y": .5}))

            email = user.get('Email', '')
            screen.get_screen('Adminhome').user_list.add_widget(
                User_data(text="Email:                   " + email, font_name="fonts/OpenSans-Semibold.ttf",
                          pos_hint={"center_x": .6, "center_y": .5}))

            screen.get_screen('Adminhome').user_list.add_widget(
                User_data(text="-------------------------------------------------------", opacity=.5))

    # other functions---------------------------------------------------------------------------------------------------

    def on_touch(self, instance):
        pass

    def on_start(self):
        Clock.schedule_once(self.start, 0)

    def carousel_autonext(self):
        screen = self.root.get_screen('Welcome-screen')
        carousel = screen.ids.carousel
        carousel.loop = True
        Clock.schedule_interval(carousel.load_next, 4)

        screen = self.root.get_screen('Home-screen')
        carousel_1 = screen.ids.carousel_1
        carousel_1.loop = True
        Clock.schedule_interval(carousel_1.load_next, 3)

    def start(self, *args):
        self.root.current = "Home-screen"
        self.carousel_autonext()
        self.display_all_user()


if __name__ == "__main__":
    TCUAdvisor().run()
