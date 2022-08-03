from pygame import *


#from time import sleep
#from tkinter import *
c_red = (255, 0, 0)
c_orange = (255, 77, 0)
c_green = (0, 255, 51)
c_lime = (0, 255, 0)
c_yellow = (255, 255, 0)
c_marine = (0, 0, 100)
c_blue = (80, 80, 255)
c_sky = (200, 255, 255) 

#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
  # конструктор класса
  def __init__(self, player_image, player_x, player_y, size_x, size_y):
      # Вызываем конструктор класса (Sprite):А
      sprite.Sprite.__init__(self)
 
      # каждый спрайт должен хранить свойство image - изображение
      self.image = transform.scale(image.load(player_image), (size_x, size_y))

      # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
      self.rect = self.image.get_rect()
      self.rect.x = player_x
      self.rect.y = player_y
 
  # метод, отрисовывающий героя на окне
  def reset(self):
      window.blit(self.image, (self.rect.x, self.rect.y))

#класс главного игрока
class Player(GameSprite):
  #метод, в котором реализовано управление спрайтом по кнопкам стрелочкам клавиатуры
  def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
      # Вызываем конструктор класса (Sprite):
      GameSprite.__init__(self, player_image, player_x, player_y,size_x, size_y)

      self.x_speed = player_x_speed
      self.y_speed = player_y_speed

  def update(self):
       ''' перемещает персонажа, применяя текущую горизонтальную и вертикальную скорость'''
       # сначала движение по горизонтали
       if packman.rect.x <= win_width-80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
         self.rect.x += self.x_speed
       # если зашли за стенку, то встанем вплотную к стене
       platforms_touched = sprite.spritecollide(self, barriers, False)
       if self.x_speed > 0: # идем направо, правый край персонажа - вплотную к левому краю стены
           for p in platforms_touched:
               self.rect.right = min(self.rect.right, p.rect.left) # если коснулись сразу нескольких, то правый край - минимальный из возможных
       elif self.x_speed < 0: # идем налево, ставим левый край персонажа вплотную к правому краю стены
           for p in platforms_touched:
               self.rect.left = max(self.rect.left, p.rect.right) # если коснулись нескольких стен, то левый край - максимальный
       if packman.rect.y <= win_height-80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
         self.rect.y += self.y_speed
       # если зашли за стенку, то встанем вплотную к стене
       platforms_touched = sprite.spritecollide(self, barriers, False)
       if self.y_speed > 0: # идем вниз
           for p in platforms_touched:
               self.y_speed = 0
               # Проверяем, какая из платформ снизу самая высокая, выравниваемся по ней, запоминаем её как свою опору:
               if p.rect.top < self.rect.bottom:
                   self.rect.bottom = p.rect.top
       elif self.y_speed < 0: # идем вверх
           for p in platforms_touched:
               self.y_speed = 0  # при столкновении со стеной вертикальная скорость гасится
               self.rect.top = max(self.rect.top, p.rect.bottom) # выравниваем верхний край по нижним краям стенок, на которые наехали
  # метод "выстрел" (используем место игрока, чтобы создать там пулю)
  def fire(self):
      bullet = Bullet('papka/pulya.png', self.rect.centerx, self.rect.top, 15, 20, 15)
      bullets.add(bullet)

#класс спрайта-врага    
class Enemy(GameSprite):
  side = "left"
  def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
      # Вызываем конструктор класса (Sprite):
      GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
      self.speed = player_speed

   #движение врага
  def update(self):
      if self.rect.x <= 420: #w1.wall_x + w1.wall_width
          self.side = "right"
      if self.rect.x >= win_width - 85:
          self.side = "left"
      if self.side == "left":
          self.rect.x -= self.speed
      else:
          self.rect.x += self.speed

# класс спрайта-пули   
class Bullet(GameSprite):
  def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
      # Вызываем конструктор класса (Sprite):
      GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
      self.speed = player_speed
  # движение врага
  def update(self):
      self.rect.x += self.speed
      # исчезает, если дойдет до края экрана
      if self.rect.x > win_width+10:
          self.kill()


'''class Nadpis(GameSprite):
    GameSprite.__init__
    pygame.font.init()
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        #self.rect = pygame.Rect(x, y, width, height)
        #self.rectamble = self.rect(x, y, width, height) #прямоугольник
        self.fill_color = color
    def color(self, new_color):
        self.fill_color = new_color
    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)
    def outline(self, frame_color, thickness, rect): #обводка существующего прямоугольника
        self.draw.rect(window, frame_color, rect, thickness)
    def fill(self):
        self.draw.rect(window, self.fill_color, self.rect)
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.image = self.font.SysFont('verdana', fsize).render(text, True, text_color)
    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))'''


#Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Лабиринт")
display.set_icon(image.load('papka/icon.png'))

window = display.set_mode((win_width, win_height))
back = (220, 165, 110)#задаем цвет согласно цветовой схеме RGB 
window.fill(back)
white = (255, 255, 255)

#создаем группу для стен
barriers = sprite.Group()

#создаем группу для пуль
bullets = sprite.Group()

#создаем группу для монстров
monsters = sprite.Group()

#создаем стены картинки
w1 = GameSprite('papka/platform2.png',win_width / 2 - win_width / 3, win_height / 2, 300, 50)
w2 = GameSprite('papka/platform2_v.png', 370, 100, 50, 400)

#добавляем стены в группу
barriers.add(w1)
barriers.add(w2)

#создаем спрайты
packman = Player('papka/alien-character.png', 5, win_height - 80, 80, 80, 0, 0)
monster = Enemy('papka/bad-character.png', win_width - 80, 180, 80, 80, 5)
final_sprite = GameSprite('papka/coin.png', win_width - 85, win_height - 100, 80, 80)

#добавляем монстра в группу
monsters.add(monster)

waittime = 150
wait = 0

#переменная, отвечающая за то, как кончилась игра
finish = False
#игровой цикл
run = True
while run:
  #цикл срабатывает каждую 0.05 секунд
    time.delay(50)
   #перебираем все события, которые могли произойти
    for e in event.get():
        if e.type == QUIT:
           run = False

        if not finish:


            if e.type == KEYDOWN:
                if e.key == K_LEFT:
                    packman.x_speed = -10
                elif e.key == K_RIGHT:
                    packman.x_speed = 10
                elif e.key == K_UP:
                    packman.y_speed = -10
                elif e.key == K_DOWN:
                    packman.y_speed = 10
                elif e.key == K_SPACE:
                    packman.fire()
                


            elif e.type == KEYUP:
                if e.key == K_LEFT:
                    packman.x_speed = 0
                elif e.key == K_RIGHT:
                    packman.x_speed = 0 
                elif e.key == K_UP:
                    packman.y_speed = 0
                elif e.key == K_DOWN:
                    packman.y_speed = 0

#проверка, что игра еще не завершена
  
      #обновляем фон каждую итерацию
    window.fill(back)#закрашиваем окно цветом


#запускаем движения спрайтов
    packman.update()
    bullets.update()

    #обновляем их в новом местоположении при каждой итерации цикла
    packman.reset()
    #рисуем стены 2
    #w1.reset()
    #w2.reset()
    bullets.draw(window)
    barriers.draw(window)
    final_sprite.reset()

    sprite.groupcollide(monsters, bullets, True, True)
    monsters.update()
    monsters.draw(window)
    sprite.groupcollide(bullets, barriers, True, False)

    #Проверка столкновения героя с врагом и стенами
    if sprite.spritecollide(packman, monsters, False):
        finish = True
        #вычисляем отношение
        img = image.load('papka/game-over.png')
        img_1 = image.load('papka/skull-and-bones.png')
        d = img.get_width() // img.get_height()
        #window.fill((255, 255, 255))
        window.blit(transform.scale(img, (win_height /2, win_height/2)), (240, 0))
        window.blit(transform.scale(img_1, (win_height /4, win_height/4)), (305, 335))

    if sprite.collide_rect(packman, final_sprite):
        finish = True
        img = image.load('papka/you-win.png')
        #window.fill((255, 255, 255))
        window.blit(transform.scale(img, (win_width/2, win_height/2)), (175, 125))


    if finish == True:
        wait = 600000
        while wait !=0:
            wait -=1
        #window.fill(white)
        my_button = GameSprite('silent.png', 300, 200, 50, 50)
        my_button.reset()
        for event in event.get():
            if event.type == MOUSEBUTTONDOWN :
                x, y = event.pos
                if my_button.collidepoint(x,y):                    
                    my_button.color(c_green) #если на карте есть надпись перекрашиваем в зелёный                       
                else: #иначе перекрашиваем в красный, 
                    my_button.color(c_red)                  

    display.update()
