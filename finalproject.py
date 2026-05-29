import flet as ft
from flet_audio import Audio
import asyncio
import random

def main(page: ft.Page):

    page.bgcolor = "black"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    title = ft.Text("Simon Says Memory Game", color="white", size=35)
    instructions = ft.Text("Watch the colors and repeat the pattern", color="white", size=16)
    status = ft.Text("Press START", color="white", size=20)
    level = ft.Text("Level: 0", color="white", size=20)
    sequence = []
    player = []
    canclick = False
    audio1 = Audio(src="Songs/d4.mp3")

    page.overlay.append(audio1)
    page.update()

    greenb = ft.Button("GREEN", bgcolor="green", color="white", width=300, height=160)
    redb = ft.Button("RED", bgcolor="red", color="white", width=300, height=160)
    blueb = ft.Button("BLUE", bgcolor="blue", color="white", width=300, height=160)
    yellowb = ft.Button("YELLOW", bgcolor="yellow", color="black", width=300, height=160)

    async def playaudio(file):
        try:
            audio1.src = file
            page.update()
            await asyncio.sleep(0.05)
            audio1.play()
        except Exception:
            pass

    async def flashgreen():
        greenb.bgcolor = "#90EE90"
        page.update()
        await playaudio("Songs/d4.mp3")
        await asyncio.sleep(0.4)
        greenb.bgcolor = "green"
        page.update()
        await asyncio.sleep(0.2)

    async def flashred():
        redb.bgcolor = "#FF7F7F"
        page.update()
        await playaudio("Songs/e4.mp3")
        await asyncio.sleep(0.4)
        redb.bgcolor = "red"
        page.update()
        await asyncio.sleep(0.2)

    async def flashblue():
        blueb.bgcolor = "#87CEFA"
        page.update()
        await playaudio("Songs/f4.mp3")
        await asyncio.sleep(0.4)
        blueb.bgcolor = "blue"
        page.update()
        await asyncio.sleep(0.2)

    async def flash_yellow():
        yellowb.bgcolor = "#FFFF99"
        page.update()
        await playaudio("Songs/g4.mp3")
        await asyncio.sleep(0.4)
        yellowb.bgcolor = "yellow"
        page.update()
        await asyncio.sleep(0.2)

    async def flash_color(color):
        if color == "green":
            await flashgreen()
        elif color == "red":
            await flashred()
        elif color == "blue":
            await flashblue()
        elif color == "yellow":
            await flash_yellow()

    async def show_sequence():
        nonlocal canclick
        canclick = False
        status.value = "Listen / Look"
        page.update()
        await asyncio.sleep(1)
        for color in sequence:
            await flash_color(color)
        status.value = "Your Turn"
        canclick = True
        page.update()

    async def next_round():
        player.clear()

        randomcolor = random.choice(["green", "red", "blue", "yellow"])
        sequence.append(randomcolor)
        level.value = "Level: " + str(len(sequence))
        page.update()
        await show_sequence()

    async def start_game(e):
        sequence.clear()
        player.clear()
        status.value = "Starting..."
        level.value = "Level: 0"
        startb.text = "START"
        page.update()

        await asyncio.sleep(1)
        await next_round()

    async def check_answer(color):
        nonlocal canclick
        if canclick == False:
            return
        await flash_color(color)

        player.append(color)
        if player != sequence[:len(player)]:
            canclick = False
            status.value = "Wrong :( Press START Again"
            startb.text = "START AGAIN"
            page.update()
            return

        if player == sequence:
            canclick = False
            status.value = "Correct :)"
            page.update()
            await asyncio.sleep(1)
            await next_round()

    async def greens(e):
        await check_answer("green")

    async def reds(e):
        await check_answer("red")

    async def blues(e):
        await check_answer("blue")

    async def yellows(e):
        await check_answer("yellow")

    greenb.on_click = greens
    redb.on_click = reds
    blueb.on_click = blues
    yellowb.on_click = yellows

    startb = ft.Button("START", on_click=start_game)
    page.add(ft.Column([title, instructions, status, level, startb, ft.Row([greenb, redb], alignment=ft.MainAxisAlignment.CENTER), ft.Row([blueb, yellowb], alignment=ft.MainAxisAlignment.CENTER)], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20))

ft.app(target=main, assets_dir="assets")