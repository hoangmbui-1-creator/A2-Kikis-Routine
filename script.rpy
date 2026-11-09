
# CHARACTERS
# ======================================================

define Kiki = Character("Kiki", color="#22a7b6")
define Angel = Character("Angel", color="#f10f0f")

# IMAGE DEFINITIONS

image bg bedroom_night = "bg bedroom_night.jpg"
image bg streetevening = "bg streetevening.jpg"
image bg_graveyard = "bg_graveyard.jpg"
image bg neighbourhood = "bg neighbourhood.jpg"
image bg neighbourhood mask = "bg neighbourhood mask.png"

image bg neighbourhood mask scaled = im.Scale(
    "bg neighbourhood mask.png",
    1280,
    720
)

# coloured window glows
image red_window_glow = Solid("#ff2020")

image red_light = "red_light.jpg"

# flaslight image
image flashlight = "flashlight.png"

#character images
image Ms Angel idle = "Ms Angel idle.png"

# graveyard hunt images 
image Object_1_crying_angel small = im.Scale(
    "Object_1_cryingangel.png",
    90,
    130
)

image Object_1_crying_angel_hover = im.Scale(
    "Object_1_cryingangel_hover.png",
    90,
    130
)

image Object_1_crying_angel normal = im.Scale(
    "Object_1_cryingangel.png",
    180,
    260
)

image Object_2_dove small = im.Scale(
    "Object_2_dove.png",
    75,
    100
)

image Object_2_dove normal = im.Scale(
    "Object_2_dove.png",
    150,
    200
)

image Object_2_dove_hover = im.Scale(
    "Object_2_dove_hover.png",
    75,
    100
)

image Object_3_lamb small = im.Scale(
    "Object_3_lamb.png",
    85,
    65
)

image Object_3_lamb normal = im.Scale(
    "Object_3_lamb.png",
    170,
    130
)

image Object_3_lamb_hover = im.Scale(
    "Object_3_lamb_hover.png",
    85,
    65
)

# red window toggles
default red_window_hover = False

transform red_pulse:
    alpha 0.25
    linear 0.6 alpha 0.85
    linear 0.6 alpha 0.25
    repeat

screen red_window_scene():

    add "bg neighbourhood"

    if red_window_hover:

        add "red_light":
            xpos 470
            ypos 260
            xsize 200
            ysize 200
            at red_pulse

    add "bg neighbourhood mask scaled"

    imagebutton:
        idle Solid("#0000")
        hover Solid("#0000")

        xpos 505
        ypos 255
        xsize 110
        ysize 80

        hovered SetVariable("red_window_hover", True)
        unhovered SetVariable("red_window_hover", False)

        action Return(True)


# VARIABLES


default found_angel = False
default found_dove = False
default found_lamb = False

default red_hover = False
default blue_hover = False
default purple_hover = False


# FLASHLIGHT SYSTEM


init python:

    class Flashlight(renpy.Displayable):

        def __init__(self):
            super(Flashlight, self).__init__()

            self.child = Transform(
                Image("flashlight.png"),
                size=(3000, 1900)
            )

            self.pos = (-1, -1)

        def render(self, width, height, st, at):

            render = renpy.Render(
                config.screen_width,
                config.screen_height
            )

            if self.pos == (-1, -1):

                render.canvas().rect(
                    "#000000",
                    (
                        0,
                        0,
                        config.screen_width,
                        config.screen_height
                    )
                )

                return render

            child_render = renpy.render(
                self.child,
                width,
                height,
                st,
                at
            )

            flashlight_width, flashlight_height = child_render.get_size()

            x, y = self.pos

            x -= flashlight_width // 2
            y -= flashlight_height // 2

            render.blit(
                child_render,
                (int(x), int(y))
            )

            renpy.redraw(self, 0)

            return render

        def event(self, ev, x, y, st):

            self.pos = (x, y)

            renpy.redraw(self, 0)

            return None

        def visit(self):

            return [self.child]


# INTRODUCTION


label start:

    scene bg bedroom_night with fade

    "3:00 AM"

    jump choice1


# WAKE UP CHOICE


label choice1:

    "Do you want to wake up?"

    menu:

        "Yes":
            jump choices1_common

        "Not yet":
            jump choices1_b

label choices1_a:

    "Good."

    return

label choices1_b:

    "..."

    jump choice2

label choice2:

    "Try again."

    menu:

        "Yes":
            jump choices1_common

label choices1_common:

    "Hurry, you don't have much time."

    scene black with fade

    Kiki "I hope it doesn't notice me."

    show Ms Angel idle at center with dissolve

    "Find _____."

    Kiki "What?"

    "We need you to hurry!"

label choice3:

    "Close your eyes again, trust us, please."

    menu:

        "who even are you-":
            jump graveyard_search


# HIDDEN OBJECT SCREEN


screen graveyard_hunt():

    add "bg_graveyard"

# CRYING ANGEL

    if not found_angel:

        imagebutton:

            idle "Object_1_crying_angel small"
            hover "Object_1_crying_angel_hover"

            xpos 250
            ypos 320

            focus_mask True

            action [
                SetVariable("found_angel", True),
                Notify("You found the Crying Angel!")
            ]

# WHITE DOVE

    if not found_dove:

        imagebutton:

            idle "Object_2_dove small"
            hover "Object_2_dove_hover"

            xpos 900
            ypos 180

            focus_mask True

            action [
                SetVariable("found_dove", True),
                Notify("You found the White Dove!")
            ]

# SLEEPING LAMB

    if not found_lamb:

        imagebutton:

            idle "Object_3_lamb small"
            hover "Object_3_lamb_hover"

            xpos 650
            ypos 560

            focus_mask True

            action [
                SetVariable("found_lamb", True),
                Notify("You found the Sleeping Lamb!")
            ]


    # WIN CONDITION

    if found_angel and found_dove and found_lamb:

        timer 1.0 action Jump("secret_passage")

    # FLASHLIGHT EFFECT

    add Flashlight()


# SEARCH AREA


label graveyard_search:

    scene bg_graveyard

    "You open your eyes to a graveyard."

    show Ms Angel idle at center with dissolve

    "Use your flashlight to search for the following relics"


    show Object_1_crying_angel normal at left with dissolve

    "The Crying Angel"

    hide Object_1_crying_angel

    show Object_2_dove normal at left with dissolve

    "The White Dove"

    hide Object_2_dove

    show Object_3_lamb normal at left with dissolve

    "The Sleeping Lamb"

    hide Object_3_lamb

    hide Ms Angel idle with dissolve

    call screen graveyard_hunt

    return


# SECRET GATE


label secret_passage:

    scene black with fade

    show Ms Angel idle at center with dissolve

    "Good."

    "But we're not quite done just yet."

    "You have to find your way back."

    Kiki "Back to where?"

    "Back to ____"

    hide Ms Angel idle with dissolve

    Kiki "What? I don't understand-"

    jump haunted_neighbourhood


# NEXT AREA


label haunted_neighbourhood:

    "You step through fog and find yourself in a familiar street block."

    scene bg neighbourhood with fade

    Kiki "The hell, this is the street I live on."

    Kiki "But something is off..."

    Kiki "The neighbour's windows look strange..."


label choice4:

    "Do you want to investigate the windows?"

    menu:
        "Yes":
            jump investigate_windows

        "No":
            jump ignore_windows


label investigate_windows:

    scene bg neighbourhood with fade

    "The correct window will glow red."

    $ result = renpy.call_screen("red_window_scene")

    if result:

        scene white
        with Dissolve(0.05)

        pause 0.08

        scene bg neighbourhood
        with Dissolve(0.05)

        "BANG!"

        jump ending_route



label ignore_windows:
    
    scene black with fade

    show Ms Angel idle at center with dissolve

    "You failed Kiki..."

    Kiki "Who are you? What are you doing to me?"

    "that's not important right now, you need to wake up."

    Kiki "Wake up? What do you mean?"

    Kiki "I WAS AWAKE."

    Kiki "You took me to a graveyard, to my own neighbourhood, but what the hell are you talking about?!"

    "Calm down, Kiki. You need to listen to me."

    "the walls are closing in, you need leave before it does."

    Kiki "Damn you. I don't know who you are, but I don't have time for your games."

    "..."

    Angel "I don't have time for your games either, Kiki."

    scene red_light with fade

    "You have failed to wake up, and now you will be trapped in this nightmare forever."

    "goodnight, Kiki."

    return

label ending_route:

    scene black with fade

    show Ms Angel idle at center with dissolve

    "Good."

    "You have found your way back."

    Kiki "What is this place? Who are you?"

    Angel "I am Angel, and I have been guiding you through this nightmare."

    Kiki "A nightmare?"

    Angel "you have changed."

    Angel "Never again follow the path of darkness, Kiki."

    Angel "You have been given a second chance, and I hope you will use it wisely."

    Kiki "wait, wait, wait... what do you mean by 'changed'?"

    Angel "the voices from 3:00 AM are gone, and you have been given a second chance."

    Kiki "I don't understand, what do you mean by 'voices'?"

    Kiki "wasn't that you, Angel? You were the one waking me up at 3:00 AM."

    Angel "No, Kiki. I was not the one waking you up at 3:00 AM."
    
    Angel "I was almost too late to reach you."

    Kiki "Then who was waking me up?"

    hide Ms Angel idle with dissolve

    Angel "Time is up child, you may leave."

    return