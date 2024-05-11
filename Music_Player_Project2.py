import os
import pygame
import tkinter as tk
from tkinter import filedialog, messagebox

class MusicPlayer:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 400
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Music Player")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("freesansbold.ttf", 18)
        self.playlist_font = pygame.font.Font("freesansbold.ttf", 14)
        self.playlist_offset = 0
        self.playlist_visible_items = 10
        self.playlist_item_height = 20
        self.playlist_scroll_speed = 2
        self.playlist = []
        self.current_index = 0
        self.music_folder = None
        self.setup_buttons()
        self.hovered_button = None
        self.button_colors = {"normal": (0, 128, 255), "hover": (0, 200, 255), "click": (0, 100, 255)}

    def load_music(self):
        if self.music_folder:
            self.playlist = []
            for file in os.listdir(self.music_folder):
                if file.endswith(".mp3"):
                    self.playlist.append(file)
            if not self.playlist:
                messagebox.showinfo("No Music Found", "No music files found in selected folder.")

    def select_music_folder(self):
        self.music_folder = filedialog.askdirectory()
        self.load_music()
        self.current_index = 0  # Reset current index
        self.stop()  # Stop current music
        self.play()  # Start playing from the new folder

    def play(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.unpause()
        else:
            if self.playlist:
                pygame.mixer.music.load(os.path.join(self.music_folder, self.playlist[self.current_index]))
                pygame.mixer.music.play()

    def pause(self):
        pygame.mixer.music.pause()

    def stop(self):
        pygame.mixer.music.stop()

    def next_track(self):
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.stop()  # Stop current music
        self.play()  # Start playing the next track

    def prev_track(self):
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.stop()  # Stop current music
        self.play()  # Start playing the previous track

    def setup_buttons(self):
        button_width = 100
        button_height = 40
        button_x = self.screen_width // 2 - button_width // 2
        play_button = pygame.Rect(20, 50, button_width, button_height)
        pause_button = pygame.Rect(140, 50, button_width, button_height)
        stop_button = pygame.Rect(260, 50, button_width, button_height)
        next_button = pygame.Rect(380, 50, button_width, button_height)
        prev_button = pygame.Rect(500, 50, button_width, button_height)
        select_folder_button = pygame.Rect(620, 50,150 , button_height)
        self.buttons = {"play": play_button, "pause": pause_button, "stop": stop_button, "next": next_button, "prev": prev_button, "select_folder": select_folder_button}

    def draw_buttons(self):
        for button_name, button_rect in self.buttons.items():
            color = self.button_colors["normal"]
            if self.hovered_button == button_name:
                color = self.button_colors["hover"]
            pygame.draw.rect(self.screen, color, button_rect)
            button_text = self.font.render(button_name.capitalize(), True, (255, 255, 255))
            text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, text_rect)

    def draw_playlist(self):
        pygame.draw.rect(self.screen, (220, 220, 220), (20, 150, self.screen_width - 40, 220))
        if self.playlist:
            start_index = self.playlist_offset
            end_index = min(start_index + self.playlist_visible_items, len(self.playlist))
            for i in range(start_index, end_index):
                y = 160 + (i - start_index) * self.playlist_item_height
                text_surface = self.playlist_font.render(self.playlist[i], True, (0, 0, 0))
                self.screen.blit(text_surface, (30, y))

    def run(self):
        running = True
        while running:
            self.screen.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        self.handle_click()
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_hover()

            self.draw_buttons()
            self.draw_playlist()
            pygame.display.flip()
            self.clock.tick(30)

    def handle_click(self):
        mouse_pos = pygame.mouse.get_pos()
        for button_name, button_rect in self.buttons.items():
            if button_rect.collidepoint(mouse_pos):
                if button_name == "play":
                    self.play()
                elif button_name == "pause":
                    self.pause()
                elif button_name == "stop":
                    self.stop()
                elif button_name == "next":
                    self.next_track()
                elif button_name == "prev":
                    self.prev_track()
                elif button_name == "select_folder":
                    self.select_music_folder()

    def handle_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        for button_name, button_rect in self.buttons.items():
            if button_rect.collidepoint(mouse_pos):
                self.hovered_button = button_name
                return
        self.hovered_button = None

if __name__ == "__main__":
    player = MusicPlayer()
    player.run()
