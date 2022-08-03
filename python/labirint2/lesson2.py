from platform import platform
from pygame import *

#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
  # конструктор класса
  def __init__(self, player_image, player_x, player_y, size_x, size_y):
      # Вызываем конструктор класса (Sprite):
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
       #если зашли за стенку, то встанем вплотную к стене
       platforms_touched = sprite.spritecollide(self, barriers, False)
       if self.y_speed > 0: # идем вниз
           for p in platforms_touched:
               self.y_speed = 0
               #Проверяем, какая из платформ снизу самая высокая, выравниваемся по ней, запоминаем её как свою опору:
               if p.rect.top < self.rect.bottom:
                   self.rect.bottom = p.rect.top
       elif self.y_speed < 0: # идем вверх
           for p in platforms_touched:
               self.y_speed = 0  # при столкновении со стеной вертикальная скорость гасится
               self.rect.top = max(self.rect.top, p.rect.bottom) # выравниваем верхний край по нижним краям стенок, на которые наехали
  def fire(self):
    bullet = Pulya('pulya.png', self.rect.centerx, self.rect.top, 10, 15)
    bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        GameSprite.__init__(self, player_image, player_x, player_y,size_x, size_y)
        self.direction = 'Left'

    def update(self):
        
        if self.rect.x >= win_width - 80:
            self.direction = 'Left'
        if self.rect.x <= 430:
            self.direction = 'Right'
        if self.direction == 'Right':
            self.rect.x += 2
        if self.direction == 'Left':
            self.rect.x -= 2

class Pulya(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        GameSprite.__init__(self, player_image, player_x, player_y,size_x, size_y)


    def update(self):
        self.rect.x += 8
        if self.rect.x >= win_width + 10:
            self.kill
        #platform_touched = sprite.groupcollide(self, barriers, True, False)
        #enemy_touched = sprite.groupcollide(self, enemy, True, True)




#Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Лабиринт")
window = display.set_mode((win_width, win_height))
back = (220, 150, 90)#задаем цвет согласно цветовой схеме RGB 

#создаем группу для стен
barriers = sprite.Group()
bullets = sprite.Group()

#создаем стены картинки
w1 = GameSprite('platform2.png',win_width / 2 - win_width / 3, win_height / 2, 300, 50)
w2 = GameSprite('platform2_v.png', 370, 100, 50, 400)

#добавляем стены в группу
barriers.add(w1)
barriers.add(w2)

#создаем спрайты
packman = Player('alien-character.png', 5, win_height - 80, 80, 80, 0, 0)
monster = Enemy('bad-character.png', win_width - 80, 180, 80, 80)
final_sprite = GameSprite('coin.png', win_width - 85, win_height - 100, 80, 80)




#переменная, отвечающая за то, как кончилась игра
finish = False
#игровой цикл
run = True
while run:

  for e in event.get():
       if e.type == QUIT:
           run = False
       elif e.type == KEYDOWN:
           if e.key == K_LEFT:
               packman.x_speed = -5
           elif e.key == K_RIGHT:
               packman.x_speed = 5
           elif e.key == K_UP :
               packman.y_speed = -5
           elif e.key == K_DOWN :
               packman.y_speed = 5
           elif e.type == K_SPACE:
               packman.fire()
                

 
       elif e.type == KEYUP:
           if e.key == K_LEFT :
               packman.x_speed = 0
           elif e.key == K_RIGHT:
               packman.x_speed = 0 
           elif e.key == K_UP:
               packman.y_speed = 0
           elif e.key == K_DOWN:
               packman.y_speed = 0

        


  if not finish:
    window.fill(back)#закрашиваем окно цветом 
    #рисуем объекты
    # w1.reset()
    # w2.reset()
    barriers.draw(window)
    
    monster.reset()
    final_sprite.reset()
    packman.reset()
    

    #включаем движение
    packman.update()
    bullets.update()
    monster.update()
    bullets.draw(window)

    sprite.groupcollide(monster, bullets, True, True)
    monster.update()
    monster.draw(window)
    sprite.groupcollide(bullets, barriers, True, False)
    #Проверка столкновения героя с врагом и стенами
    if sprite.collide_rect(packman, monster):
        finish = True
        #вычисляем отношение
        img = image.load('game-over.png')
        d = img.get_width() // img.get_height()
        window.fill((255, 255, 255))
        window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))

    if sprite.collide_rect(packman, final_sprite):
        finish = True
        img = image.load('you-win.png')
        window.fill((255, 255, 255))
        window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
  
  #цикл срабатывает каждую 0.05 секунд
  time.delay(50)
  
  display.update()