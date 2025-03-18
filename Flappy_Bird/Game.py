import pygame
import random
import os

# Pygame'i başlat
pygame.init()

# En üstte pygame.mixer'ı başlatalım
pygame.mixer.init()

# Asset dizinini kontrol et
ASSET_DIR = "assets"
if not os.path.exists(ASSET_DIR):
    print(f"Hata: {ASSET_DIR} klasörü bulunamadı!")
    exit()

# Ekran boyutları
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Farklı kuş sprite'ları
BIRD_SPRITES = {
    'Phoenix': pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "bird.png")), (60, 45)),
    'Shadow': pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "bird2.png")), (60, 45)),
    'Storm': pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "bird3.png")), (60, 45)),
    'Crystal': pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "bird4.png")), (60, 45)),
    'Dragon': pygame.transform.scale(pygame.image.load(os.path.join(ASSET_DIR, "bird5.png")), (60, 45))
}

# Global değişkenler
selected_bird = 'Phoenix'  # Varsayılan kuş
has_selected_character = False  # Karakter seçilip seçilmediğini kontrol eden değişken

BACKGROUND = pygame.image.load(os.path.join(ASSET_DIR, "background.png"))
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
PIPE_IMG = pygame.image.load(os.path.join(ASSET_DIR, "pipe.png"))

# Pipe sprite'ını yükle ve boyutlandır
PIPE_IMG = pygame.transform.scale(PIPE_IMG, (70, 500))  # Boru genişliği ve örnek yükseklik
# Alt boru için sprite'ı ters çevir
PIPE_IMG_INVERTED = pygame.transform.flip(PIPE_IMG, False, True)

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (135, 206, 235)

# Buton renkleri ve font
BUTTON_COLOR = (70, 189, 255)  # Açık mavi
BUTTON_HOVER_COLOR = (30, 144, 255)  # Koyu mavi
BUTTON_TEXT_COLOR = (255, 255, 255)  # Beyaz
SCORE_COLOR = (255, 215, 0)  # Altın rengi
TITLE_COLOR = (255, 255, 255)  # Beyaz

# Ses dosyalarını kontrol et ve yükle
try:
    SOUNDS = {
        'jump': pygame.mixer.Sound(os.path.join(ASSET_DIR, "jump.mp3")),
        'score': pygame.mixer.Sound(os.path.join(ASSET_DIR, "point.mp3")),
        'hit': pygame.mixer.Sound(os.path.join(ASSET_DIR, "hit.mp3")),
        'wing': pygame.mixer.Sound(os.path.join(ASSET_DIR, "wing.mp3"))
    }
    
    # Arka plan müziği
    pygame.mixer.music.load(os.path.join(ASSET_DIR, "background.mp3"))
    
except Exception as e:
    print(f"Ses dosyalarını yüklerken hata oluştu: {e}")
    print("Lütfen assets klasöründeki ses dosyalarının isimlerini kontrol edin.")
    exit()

# Ses seviyelerini ayarla
for sound in SOUNDS.values():
    sound.set_volume(0.3)

pygame.mixer.music.set_volume(0.1)

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.is_hovered = False
        self.shadow_offset = 2

    def draw(self, screen):
        # Gölge efekti
        shadow_rect = self.rect.copy()
        shadow_rect.x += self.shadow_offset
        shadow_rect.y += self.shadow_offset
        pygame.draw.rect(screen, (0, 0, 0, 128), shadow_rect, border_radius=12)
        
        # Ana buton
        color = BUTTON_HOVER_COLOR if self.is_hovered else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        
        # Parlama efekti
        if self.is_hovered:
            pygame.draw.rect(screen, (255, 255, 255, 64), self.rect, border_radius=12, width=2)
        
        # Buton metni
        text_surface = self.font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class BirdSelector:
    def __init__(self):
        self.birds = list(BIRD_SPRITES.keys())
        self.current_index = 0
        
        # Seçim butonları
        self.left_button = Button(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2, 40, 40, "<")
        self.right_button = Button(SCREEN_WIDTH//2 + 110, SCREEN_HEIGHT//2, 40, 40, ">")
        self.select_button = Button(SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 + 100, 120, 40, "Seç")
        self.back_button = Button(10, 10, 100, 40, "Geri")
    
    def draw(self, screen):
        # Başlık
        font = pygame.font.Font(None, 48)
        title = font.render("Karakter Seçimi", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
        
        # Gölgeli başlık
        shadow_title = font.render("Karakter Seçimi", True, BLACK)
        shadow_rect = title_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        screen.blit(shadow_title, shadow_rect)
        screen.blit(title, title_rect)
        
        # Kuş sprite'ını göster
        current_bird = BIRD_SPRITES[self.birds[self.current_index]]
        bird_rect = current_bird.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(current_bird, bird_rect)
        
        # Kuş adını göster
        name_font = pygame.font.Font(None, 36)
        name = name_font.render(self.birds[self.current_index], True, SCORE_COLOR)
        name_rect = name.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        
        # Gölgeli isim
        shadow_name = name_font.render(self.birds[self.current_index], True, BLACK)
        shadow_name_rect = name_rect.copy()
        shadow_name_rect.x += 2
        shadow_name_rect.y += 2
        screen.blit(shadow_name, shadow_name_rect)
        screen.blit(name, name_rect)
        
        # Butonları çiz
        self.left_button.draw(screen)
        self.right_button.draw(screen)
        self.select_button.draw(screen)
        self.back_button.draw(screen)
    
    def handle_events(self, event):
        global selected_bird
        
        if self.back_button.handle_event(event):
            return 'back'
        if self.left_button.handle_event(event):
            self.current_index = (self.current_index - 1) % len(self.birds)
        elif self.right_button.handle_event(event):
            self.current_index = (self.current_index + 1) % len(self.birds)
        elif self.select_button.handle_event(event):
            selected_bird = self.birds[self.current_index]
            return 'select'
        return None

# Kuş özellikleri
class Bird:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.gravity = 0.5
        self.jump_strength = -10
        self.size = 45
        self.alive = True
        self.rotation = 0
        self.sprite = BIRD_SPRITES[selected_bird]  # Seçili kuşu kullan

    def jump(self):
        SOUNDS['jump'].play()  # Zıplama sesi
        self.velocity = self.jump_strength
        self.rotation = 45  # Zıplarken yukarı bak

    def move(self):
        self.velocity += self.gravity
        self.y += self.velocity
        
        # Kuşun rotasyonunu güncelle
        if self.velocity < 0:
            self.rotation = 45
        else:
            self.rotation = max(-90, self.rotation - 5)  # Düşerken aşağı bak

    def draw(self, screen):
        # Sprite'ı döndür
        rotated_sprite = pygame.transform.rotate(self.sprite, self.rotation)
        # Sprite'ın merkezini hesapla
        rect = rotated_sprite.get_rect(center=(self.x + self.size//2, self.y + self.size//2))
        screen.blit(rotated_sprite, rect)

    def check_collision(self, pipe):
        # Kuş dikdörtgeni - boyutu biraz küçült için daha hassas çarpışma
        bird_rect = pygame.Rect(self.x + 10, self.y + 10, self.size - 20, self.size - 20)
        
        # Üst boru dikdörtgeni
        top_pipe = pygame.Rect(pipe.x, 0, pipe.WIDTH, pipe.height - pipe.GAP)
        
        # Alt boru dikdörtgeni
        bottom_pipe = pygame.Rect(pipe.x, pipe.height, pipe.WIDTH, SCREEN_HEIGHT - pipe.height)
        
        # Çarpışma kontrolü
        if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe):
            return True
            
        # Ekran sınırları kontrolü
        if self.y <= 0 or self.y + self.size >= SCREEN_HEIGHT:
            return True
            
        return False

# Boru özellikleri
class Pipe:
    def __init__(self):
        self.GAP = 250
        self.WIDTH = 70  # Sprite genişliğiyle uyumlu olmalı
        self.x = SCREEN_WIDTH
        self.height = random.randint(200, 500)
        self.sprite = PIPE_IMG
        self.sprite_inverted = PIPE_IMG_INVERTED
        self.scored = False  # Borudan geçişi kontrol etmek için

    def move(self):
        self.x -= 3

    def draw(self, screen):
        # Üst boru (ters çevrilmiş)
        screen.blit(self.sprite_inverted, (self.x, self.height - self.GAP - 500))
        # Alt boru
        screen.blit(self.sprite, (self.x, self.height))

def draw_score(screen, score, x, y, is_game_over=False):
    font_size = 74 if is_game_over else 50
    font = pygame.font.Font(None, font_size)
    
    # Gölgeli skor metni
    shadow_text = font.render(f"Skor: {score}", True, (0, 0, 0))
    text = font.render(f"Skor: {score}", True, SCORE_COLOR)
    
    # Gölgeyi çiz
    screen.blit(shadow_text, (x + 2, y + 2))
    # Ana metni çiz
    screen.blit(text, (x, y))

def main_menu():
    global has_selected_character
    start_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50, 200, 50, "Başlat")
    character_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 20, 200, 50, "Karakterler")
    quit_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 90, 200, 50, "Çıkış")
    
    running = True
    while running:
        SCREEN.blit(BACKGROUND, (0, 0))
        
        # Başlık
        font = pygame.font.Font(None, 100)
        title_shadow = font.render("Flappy Bird", True, (0, 0, 0))
        title = font.render("Flappy Bird", True, TITLE_COLOR)
        
        # Gölgeli başlık
        title_rect = title_shadow.get_rect(center=(SCREEN_WIDTH//2 + 3, SCREEN_HEIGHT//4 + 3))
        SCREEN.blit(title_shadow, title_rect)
        
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
        SCREEN.blit(title, title_rect)
        
        # Seçili karakteri göster
        if has_selected_character:
            char_font = pygame.font.Font(None, 36)
            char_text = char_font.render(f"Seçili Karakter: {selected_bird}", True, SCORE_COLOR)
            char_rect = char_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
            SCREEN.blit(char_text, char_rect)
        
        start_button.draw(SCREEN)
        character_button.draw(SCREEN)
        quit_button.draw(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if start_button.handle_event(event):
                if not has_selected_character:
                    # Karakter seçilmemişse karakter seçim ekranına yönlendir
                    result = bird_selection_screen()
                    if not result:
                        return False
                    elif result == 'start_game':
                        return True  # Oyunu başlat
                else:
                    # Karakter seçilmişse direkt oyunu başlat
                    return True
            if character_button.handle_event(event):
                result = bird_selection_screen()
                if not result:
                    return False
                elif result == 'start_game':
                    return True  # Oyunu başlat
                has_selected_character = True
            if quit_button.handle_event(event):
                return False
        
        pygame.display.flip()

def game_over_screen(score):
    pygame.mixer.music.stop()  # Müziği durdur
    SOUNDS['hit'].play()  # Game over sesi
    menu_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2, 200, 50, "Ana Sayfaya Dön")
    quit_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 100, 200, 50, "Çıkış")
    
    while True:
        SCREEN.blit(BACKGROUND, (0, 0))
        
        # Game Over yazısı
        font_big = pygame.font.Font(None, 100)
        shadow_text = font_big.render("Game Over", True, (0, 0, 0))
        game_over_text = font_big.render("Game Over", True, (255, 50, 50))  # Kırmızımsı renk
        
        # Gölgeli Game Over
        shadow_rect = shadow_text.get_rect(center=(SCREEN_WIDTH//2 + 3, SCREEN_HEIGHT//4 + 3))
        SCREEN.blit(shadow_text, shadow_rect)
        
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
        SCREEN.blit(game_over_text, game_over_rect)
        
        # Skor gösterimi
        draw_score(SCREEN, score, SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//3, True)
        
        menu_button.draw(SCREEN)
        quit_button.draw(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if menu_button.handle_event(event):
                return 'menu'  # Ana menüye dönüş için yeni değer
            if quit_button.handle_event(event):
                return False
        
        pygame.display.flip()

def countdown_screen():
    numbers = [(3, (255, 0, 0)), (2, (255, 165, 0)), (1, (0, 255, 0))]  # (sayı, renk) tuple'ları
    
    for number, color in numbers:
        start_time = pygame.time.get_ticks()
        
        while pygame.time.get_ticks() - start_time < 1000:  # Her sayı 1 saniye gösterilir
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
            
            SCREEN.blit(BACKGROUND, (0, 0))
            
            # Sayıyı ekrana çiz
            font = pygame.font.Font(None, 150)
            number_text = font.render(str(number), True, color)
            number_rect = number_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            SCREEN.blit(number_text, number_rect)
            
            pygame.display.flip()
    
    return True

def bird_selection_screen():
    selector = BirdSelector()
    
    running = True
    while running:
        SCREEN.blit(BACKGROUND, (0, 0))
        
        selector.draw(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            result = selector.handle_events(event)
            if result == 'back':
                return True
            elif result == 'select':
                global has_selected_character
                has_selected_character = True
                return 'start_game'  # Yeni dönüş değeri ekledik
        
        pygame.display.flip()

# Pause butonu için yeni bir sınıf oluşturalım
class PauseButton:
    def __init__(self):
        self.size = 30
        self.x = SCREEN_WIDTH - 40  # Sağ üst köşeden 40 piksel içeride
        self.y = 10  # Üstten 10 piksel aşağıda
        self.paused = False
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        
    def draw(self, screen):
        # Buton arka planı
        pygame.draw.rect(screen, BUTTON_COLOR, self.rect, border_radius=5)
        
        # Pause/Play simgesi
        if not self.paused:
            # Pause simgesi (iki dikey çizgi)
            pygame.draw.rect(screen, WHITE, (self.x + 8, self.y + 7, 4, 16))
            pygame.draw.rect(screen, WHITE, (self.x + 18, self.y + 7, 4, 16))
        else:
            # Play simgesi (üçgen)
            points = [(self.x + 10, self.y + 7),
                     (self.x + 10, self.y + 23),
                     (self.x + 22, self.y + 15)]
            pygame.draw.polygon(screen, WHITE, points)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.paused = not self.paused
                return True
        return False

def pause_menu():
    resume_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2, 200, 50, "Ana Menüye Dön")
    quit_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 100, 200, 50, "Çıkış")
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if resume_button.handle_event(event):
                return 'menu'
            if quit_button.handle_event(event):
                return False
        
        resume_button.draw(SCREEN)
        quit_button.draw(SCREEN)
        pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    
    while True:
        has_selected_character = False
        if not main_menu():
            break
            
        pygame.mixer.music.play(-1)
        
        if not bird_selection_screen():
            break
        
        bird = Bird()
        pipes = []
        pipe_spawn_timer = 0
        running = True
        score = 0
        pause_button = PauseButton()  # Pause butonu oluştur
        
        bg_x = 0
        bg_speed = 1

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and bird.alive:
                    bird.jump()
                if pause_button.handle_event(event):  # Pause butonuna tıklanma kontrolü
                    if pause_button.paused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                    continue

            # Oyun duraklatılmışsa güncelleme yapma
            if pause_button.paused:
                # Sadece ekranı yeniden çiz
                SCREEN.blit(BACKGROUND, (bg_x, 0))
                SCREEN.blit(BACKGROUND, (bg_x + SCREEN_WIDTH, 0))
                for pipe in pipes:
                    pipe.draw(SCREEN)
                bird.draw(SCREEN)
                draw_score(SCREEN, score, 10, 10)
                pause_button.draw(SCREEN)
                pygame.display.flip()
                clock.tick(60)
                continue

            if bird.alive:
                bird.move()

                bg_x -= bg_speed
                if bg_x <= -SCREEN_WIDTH:
                    bg_x = 0

                pipe_spawn_timer += 1
                if pipe_spawn_timer > 90:
                    pipes.append(Pipe())
                    pipe_spawn_timer = 0

                # Boruları hareket ettir ve kontrol et
                for pipe in pipes[:]:
                    pipe.move()
                    
                    # Skor kontrolü
                    if not pipe.scored and pipe.x + pipe.WIDTH < bird.x:
                        score += 1
                        pipe.scored = True
                        SOUNDS['score'].play()  # Puan kazanma sesi
                    
                    # Çarpışma kontrolü
                    if bird.check_collision(pipe):
                        SOUNDS['hit'].play()  # Çarpışma sesi
                        bird.alive = False
                        pygame.mixer.music.stop()  # Müziği durdur
                        # Oyun sonu ekranını göster
                        result = game_over_screen(score)
                        if result == 'menu':
                            running = False  # Ana menüye dön
                        elif not result:
                            return  # Oyundan çık
                        break
                
                # Ekrandan çıkan boruları sil
                for pipe in pipes[:]:
                    if pipe.x + pipe.WIDTH < 0:
                        pipes.remove(pipe)

            # Çizim işlemleri
            SCREEN.blit(BACKGROUND, (bg_x, 0))
            SCREEN.blit(BACKGROUND, (bg_x + SCREEN_WIDTH, 0))
            
            for pipe in pipes:
                pipe.draw(SCREEN)
            
            bird.draw(SCREEN)
            
            # Skor gösterimi güncellendi
            draw_score(SCREEN, score, 10, 10)
            pause_button.draw(SCREEN)  # Pause butonunu çiz
            
            pygame.display.flip()
            clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
