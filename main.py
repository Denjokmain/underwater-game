from init import *
from engine import *
from time import time
from random import randint
from math import cos,sin,radians, degrees, atan2

pg.mixer.init()

# получает угол между точками
def getAngle(a, b, c):
    ang = degrees(atan2(c[1]-b[1], c[0]-b[0]) - atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang

# ставит элемент по центру
def setElementToCenterX(element):
    try:
        element.setPos(x=sc.get_width()/2 - element.model.get_width()/2)
    except:
        element.setPos(x=sc.get_width()/2 - element.w/2)

# ставит максимальный размер картинки без изменения соотношения сторон
def setMaxScreenSizeToElement(image):
    w, h = sc.get_size()

    if w/image.w <= h/image.h:
        multiplier = w/image.w
        image.x = 0; image.y = (h - image.h * multiplier) / 2
    else:
        multiplier = h/image.h
        image.x = (w - image.w * multiplier) / 2; image.y = 0
    image.resize(image.w*multiplier, image.h*multiplier)
    return multiplier

# диалоговое окно
class DialogManager:
    bg = Image('images/dialogBg.png', 0, 0, 4000, 300, True)
    talkImageSize = (70, 70)
    work = False
    def start(self, gameMap, text, letterWriteTime=.1, firstWaitTime=1, talkImage=None, talkImagePos=(.1, .1)):
        try:
            for i in self.labels:
                self.map.delElement(i)
        except:
            pass
        
        self.bg.resize(h=300)
        self.map = gameMap
        self.text = text
        self.labels = [Label("", x=self.talkImageSize[0]+10, color=(240, 240, 240), anchor=True)]
        self.time = time() + firstWaitTime
        self.letterWriteTime = letterWriteTime
        self.map.addElement([self.labels[-1]])
        self.image = None
        if talkImage:
            self.image = Image(f'images/{talkImage}', 10, self.bg.y + self.bg.h - self.talkImageSize[1],*self.talkImageSize, True)
            self.map.addElement(self.image)
        self.map.eventHandler.onLoopUpdate.addElement(self.showDialog)
        self.work = True
    
    def stop(self):
        self.map.eventHandler.onLoopUpdate.delElement(self.showDialog)
        for i in self.labels:
            self.map.delElement(i)
        for i in self.labels[1:]:
            self.labels.remove(i)
        if self.image:
            self.map.delElement(self.image)
        self.map.delElement(self.bg)
        self.work = False

    def showDialog(self):
        self.work = True
        self.map.delElement(self.bg)
        for i in self.labels:
            self.map.delElement(i)
        for i in self.labels[1:]:
            self.labels.remove(i)
        self.map.addElement(self.bg)
        if self.image:
            self.map.delElement(self.image)
            self.map.addElement(self.image)
        k = 0
        text = ''
        w,h = sc.get_size()
        for i in self.text:
            if k > (time() - self.time) // self.letterWriteTime:
                break
            if self.labels[-1].font.size(text)[0] >= w - self.talkImageSize[0] - 30:
                self.labels[-1].updateText(" ".join(text.split()[:-1]))
                self.labels.append(Label("", x=self.talkImageSize[0]+10, y=self.labels[-1].y + 30, color=(240, 240, 240), anchor=True))
                text = text.split()[-1:][0]

            text += i
            self.labels[-1].updateText(text)
            k += 1
        for i in self.labels:
            self.map.addElement(i)
        self.bg.resize(sc.get_size()[0], 120)
        if self.image:
            self.image.setPos(10, self.bg.h - self.image.h)

    def onResize(self):
        pass

# основной код
class GameStory:
    # каждый класс новая карта
    class Story0:
        # сбросс данных карты
        def reset(self):
            try: self.myMap.clear()
            except: pass
        
        # запускающая все механики функция
        def start(self):
            self.nextDialogTime = [time(), 0]
            game.setMap('дом')
            self.myMap = game.getMap('дом')
            self.reset()
            self.myMap.resize(*homeFirstSize)

            self.oldManPos = (.72, .6)
            self.heroPos = (.2, .76)
            mapW, mapH = self.myMap.w, self.myMap.h
            self.oldMan = Image(['images/old-man-sitting.png', 'images/old-man-sitting1.png'], mapW*self.oldManPos[0], mapH*self.oldManPos[1], 100, 100)
            self.hero = Image(['images/hero-laying.png', 'images/hero-sitting.png', 'images/hero1.png'], mapW*self.heroPos[0], mapH*self.heroPos[1], 90, 90)

            self.currentDialog = -1
            # время сколько будет идти диалог, функция выполняемая по запуску диалога, текст, скорость печатания буквы, пауза перел началом диалона, картинка
            self.dialogs = [
                [(3, None), 'Мхмхм', .08, 1, 'hero-cut1.png'],
                [(5, self.heroNextImage), '(Неужели я переиграл в игры и отрубился на полу)', .03, .6, 'hero-cut0.png'],
                [(8.4, None), 'Мдам и как ты заснул на полу, ну да ладно. Пока ты спал я полазил на складе и нашел акваланг, не хочешь посмотреть ?', .05, .7, 'old-man-cut0.png'],
                [(5, None), 'Конечно хочу, а где он ?', .06, .6, 'hero-cut0.png'],
                [(4.6, self.heroNextImage), 'Вот он, держи примерь', .06, .6, 'old-man-cut1.png'],
                [(4.6, self.heroNextImage), 'Воу в нем так приколько', .06, .6, 'hero-cut2.png'],
                [(10, None), 'Рад что тебе понравился, у меня как раз есть одна просба, не мог бы ты помочь достать сундук с воды который я случайно обронил ?', .06, .8, 'old-man-cut0.png'],
                [(4.6, None), 'Конечно, отправляемся прямо сейчас', .06, .6, 'hero-cut2.png'],
                ]
            self.heroImages = [1, 1, 2]
            
            # добавление елементов в обработчика событиый
            self.myMap.addElement([self.oldMan, self.hero])
            self.myMap.eventHandler.onLoopUpdate.addElement(self.onResize)
            self.myMap.eventHandler.onLoopUpdate.addElement(self.dialogAutoUpdate)
            self.myMap.eventHandler.onClick.addElement(self.myMap, self.nextDialog)

        def heroNextImage(self):
            self.hero.changeImage(self.heroImages[0])
            self.heroImages.pop(0)
            if len(self.heroImages) == 1:
                self.oldMan.changeImage(1)
            elif len(self.heroImages) == 0:
                self.oldMan.changeImage(0)

        # меняет диалоговый текст беря данные с переменной self.dialogs
        def nextDialog(self, *args):
            self.currentDialog += 1
            if len(self.dialogs) > self.currentDialog:
                self.nextDialogTime = [time(), self.dialogs[self.currentDialog][0][0]]
                if self.dialogs[self.currentDialog][0][1]:
                    self.dialogs[self.currentDialog][0][1]()
                dialogManager.start(self.myMap, *self.dialogs[self.currentDialog][1:])
            else:
                dialogManager.stop()
                self.myMap.eventHandler.onClick.delElement(self.myMap)
                self.myMap.eventHandler.onLoopUpdate.delElement(self.dialogAutoUpdate)
                darkScreenAnimation.newStory(gameStory.Story1())
                setLvl(1)

        def dialogAutoUpdate(self):
            self.nextDialogTime[1] -= time() - self.nextDialogTime[0]
            self.nextDialogTime[0] = time()
            if self.nextDialogTime[1] <= 0:
                self.nextDialog()
        
        def onResize(self, *args):
            w, h = sc.get_size()
            if (self.myMap.w != w) & (self.myMap.h != h):
                multiplier = setMaxScreenSizeToElement(self.myMap)
                mapW, mapH = self.myMap.w, self.myMap.h

                self.oldMan.resize(self.oldMan.w*multiplier, self.oldMan.h*multiplier)
                self.oldMan.setPos(mapW*self.oldManPos[0], mapH*self.oldManPos[1])

                self.hero.resize(self.hero.w*multiplier, self.hero.h*multiplier)
                self.hero.setPos(mapW*self.heroPos[0], mapH*self.heroPos[1])

    class Story1:
        def reset(self):
            try:
                self.myMap.x = 0
                self.myMap.y = 0
                self.myMap.clear()
            except:
                pass

        def start(self):
            self.respawn = None
            self.nextDialogTime = [time(), 0]
            game.setMap('вода 0')
            self.myMap = game.getMap('вода 0')
            self.reset()
            self.myMap.addElement(waterRect)

            self.borders = [
                selfRect(-100, 500)
            ]

            self.chest = Image(['images/chest.png', 'images/chest-open.png'], 50, self.myMap.h - 60, 60, 60)
            self.chestBg = Image('images/chest-floor.png', 0, 0, 4000, 2000)
            self.isChestOpen = False; self.isFoundChest = False
            self.book = Image('images/book0.png', 200, 160, 400, 400)
            self.sand = Image('images/sand.png', -1000, self.myMap.h, self.myMap.w + 2000, 800)
            self.chestHoverText = Button('Нажмите что бы открыть', 30, self.chest.y, fontSize=16)
            self.oldMan = Image('images/old-man.png', -40, 380, 100, 100)
            self.hero = Image(['images/hero.png', 'images/hero1.png', *[f'images/hero-jump{i}.png' for i in range(11)], 'images/hero2.png', 'images/hero4.png'], -14, 386, 90, 90)
            self.boat = Image('images/boat.png', -50, 370, 160, 160)
            self.jumpTime = .06
            self.startJumpTime = 0

            self.lines = []
            for i in range(4):
                self.lines.append([])
                for j in range((self.myMap.w) // 200):
                    self.lines[-1].append(selfRect(50 + j*200 + randint(-50, 50), 300 + 230*i + randint(-50, 50), 10, 2, (240, 240, 240)))
                    self.myMap.addElement(self.lines[-1][-1])

            self.dialogs = [
                [(3.6, self.dialogSkip), 'Ну что, ты готов ?', .06, .6, 'old-man-cut0.png'],
                [(3.8, None), 'Щас только акваланг одену', .06, .6, 'hero-cut0.png'],
                [(3.6, self.setHeroImage), 'Воо теперь готов', .06, .6, 'hero-cut2.png'],
                [(5, None), 'Уоп нежданчик, управление на (W,A,S,D)', .03, -.03, 'robot.png'],
                [(5, None), 'Поплылии!!', .06, .6, 'hero-cut2.png'],
            ]
            self.actions = [
                self.mooveBoat, self.nextDialog, self.nextDialog, self.jumpToWater, self.mooveHero, 
                self.nextDialog, self.mooveHero, self.nextDialog, self.nextDialog
            ]
            self.heroMooveY = 1
            self.myMap.addElement([self.oldMan, self.hero, self.boat, self.sand])
            self.myMap.eventHandler.onLoopUpdate.addElement(self.actionsPlay)
            self.spawnDecor()

        def spawnDecor(self):
            try:
                for i in self.fish:
                    if i[1][0] > i[0].x:
                        i[0].moove(1)
                        if i[2]: i[0].flip(); i[2] = False
                    elif i[1][0] == i[0].x:
                        pass
                    else:
                        i[0].moove(-1)
                        if not i[2]: i[0].flip(); i[2] = True
                    if i[1][1] > i[0].y:
                        i[0].moove(y=1)
                    elif i[1][1] == i[0].y:
                        pass
                    else:
                        i[0].moove(y=-1)   
                    if (i[0].x == i[1][0]) & (i[0].y == i[1][1]):
                        i[1] = [int(randint(50, self.myMap.w - 100)), int(randint(500, self.myMap.h - 100))]
            except:
                self.decor = []
                for i in range(5):
                    size = randint(300, 800)
                    self.decor.append(Image(f'images/stone{randint(0, 1)}.png', randint(100, self.myMap.w - 70), self.myMap.h-size/2, size, size/2))
                    while self.decor[-1].collideobjects(self.decor[:-1]):
                        self.decor[-1].setPos(randint(100, self.myMap.w - 70))
                    self.myMap.addElement(self.decor[-1])
                self.myMap.addElement(self.chest)
                self.fish = []
                for i in range(20):
                    size = randint(30, 50)
                    self.decor.append(Image(f'images/leaves{randint(0, 3)}.png', randint(100, self.myMap.w - 70), self.myMap.h-size, size, size))
                    self.myMap.addElement(self.decor[-1])
                for i in range(14):
                    pos = [int(randint(50, self.myMap.w - 100)), int(randint(500, self.myMap.h - 100))]
                    pos2 = [int(randint(50, self.myMap.w - 100)), int(randint(500, self.myMap.h - 100))]
                    self.fish.append([Image(f'images/fish{randint(0, 7)}.png', *pos, 30, 30), pos2, False])
                    self.myMap.addElement(self.fish[-1][0])
                self.myMap.eventHandler.onLoopUpdate.addElement(self.spawnDecor)

        def borderRespawn(self):
            if self.respawn == None:
                self.respawn = time() + .6
            try:
                for i in self.mermaid[:4]:
                    i.moove(4)
                for i in self.mermaid[4:]:
                    i.moove(-4)

            except:
                self.mermaid = []
                x = -600
                for i in range(4):
                    self.mermaid.append(Image('images/mermaid.png', x, 300 + 220 * i, 130, 130))
                x = self.myMap.w + 600
                for i in range(4):
                    self.mermaid.append(Image('images/mermaid.png', x, 300 + 220 * i, 130, 130))
                self.myMap.addElement(self.mermaid)

        def showChestText(self, *args):
            self.myMap.addElement(self.chestHoverText)
            
        def hideChestText(self, *args):
            self.myMap.delElement(self.chestHoverText)

        def openChest(self, *args):
            self.chest.changeImage(1)
            self.myMap.anchorCameraAtElement()
            self.myMap.addElement([self.chestBg, self.book])
            self.myMap.x = 0
            self.myMap.y = 0
            self.isChestOpen = True; self.isFoundChest = True
            self.nextDialogTime[1] = 0
            self.dialogs = [
                [(6, self.closeChest), '... Здесь только книга, отнесука я её дедушке', .06, 1, 'hero-cut2.png'],
            ]
            self.actions.pop(0)
            self.myMap.eventHandler.onClick.delElement(self.chest)
            self.myMap.eventHandler.mouseHover.delElement(self.chest)

        def closeChest(self, *args):
            self.myMap.anchorCameraAtElement(self.hero)
            self.myMap.delElement(self.chestBg)
            self.myMap.delElement(self.book)
            self.isChestOpen = False
            self.myMap.delElement(self.chestHoverText)

        def dialogSkip(self, *args):
            self.myMap.eventHandler.onClick.addElement(self.myMap, self.resetDialogTime)

        def resetDialogTime(self, *args):
            self.nextDialogTime[1] = .001

        def goHomeStart(self):
            darkScreenAnimation.newStory(gameStory.Story2())
            self.actions = [self.goHome]

        def goHome(self):
            self.actions = [self.goHome]
            self.boat.moove(-2)
            self.hero.moove(-2)
            self.oldMan.moove(-2)
           
        def mooveHero(self):
            if (self.hero.x < 0) or (self.hero.x > self.myMap.w):
                self.borderRespawn()
            if self.respawn != None:
                if type(self.respawn) == str:
                    pass
                else:
                    if time() > self.respawn:
                        if difficultSetting.actionAfterDie == 'respawn':
                            darkScreenAnimation.newStory(gameStory.Story1())
                        else:
                            darkScreenAnimation.newStory(gameStory.Story0())
                        self.respawn = "a"
            if dialogManager.work: dialogManager.stop()
            if not self.isChestOpen:
                keys.updateKeys()
                speed = 3
                x, y = [(-keys.a + keys.d) * speed, (-keys.w + keys.s) * speed]
                if y == 0:
                    y = 1
                if x >= 1: self.hero.changeImage(1)
                if x <= -1: self.hero.changeImage(14)
                self.hero.moove(x, y)
                if self.hero.y > self.myMap.h - self.hero.h: self.hero.setPos(y=self.myMap.h - self.hero.h)
                if self.hero.y < 500: self.hero.setPos(y=500)
                if self.isFoundChest:
                    if self.oldMan.x + 200 >= self.hero.x >= self.oldMan.x - 100:
                        if self.hero.colliderect(self.boat):
                            self.dialogs = [
                                [(5, None), 'Там в сундуке была только книга', .06, .6, 'hero-cut0.png'],
                                [(7, None), 'Мне эта книга что то напоминает, поплыли домой а я потом тебе расскажу о чём там', .06, .6, 'old-man-cut0.png'],
                                [(5, self.goHomeStart), ' ', .06, .6],
                                [(5, None), ' ', .06, .6],
                            ]
                            self.actions.pop(0)
                            self.hero.changeImage(13)
                            self.hero.setPos(self.oldMan.x + 60, self.oldMan.y + 16)
                            setLvl(2)
            
        def setHeroImage(self):
            self.hero.changeImage(1)

        def mooveBoat(self):
            if self.boat.x < 600:
                self.boat.moove(2)
                self.hero.moove(2)
                self.oldMan.moove(2)
            else:
                self.actions.pop(0)

        def jumpToWater(self):
            if (self.hero.imgIndex < 12):
                if self.jumpTime <= time() - self.startJumpTime:
                    self.startJumpTime = time()
                    self.hero.changeImage(self.hero.imgIndex+1)

            if self.hero.x < 750:
                self.hero.moove(3, -1)
            elif self.hero.y >= self.myMap.h - self.hero.h:
                self.myMap.eventHandler.onClick.addElement(self.chest, self.openChest)
                self.myMap.eventHandler.mouseHover.addElement(self.chest, self.showChestText, self.hideChestText)
                self.actions.pop(0)
                dialogManager.stop()
                self.hero.changeImage(1)
            else:
                self.heroMooveY += .06
                if self.heroMooveY > 5:
                    self.heroMooveY = 5
                self.hero.moove(1, self.heroMooveY)
                w, h = sc.get_size()
                if self.hero.y > h/2 - self.hero.h/2:
                    self.myMap.anchorCameraAtElement(self.hero)
       
        def nextDialog(self, *args):
            if not self.isChestOpen:        
                if len(self.dialogs) > 1:
                    if self.nextDialogTime[1] <= 0:
                        self.nextDialogTime = [time(), self.dialogs[0][0][0]]
                        dialogManager.start(self.myMap, *self.dialogs[0][1:])
                        if self.dialogs[0][0][1]:
                            self.dialogs[0][0][1]()
                    else:
                        self.nextDialogTime[1] -= time() - self.nextDialogTime[0]
                        self.nextDialogTime[0] = time()
                if self.nextDialogTime[1] <= 0:
                    if len(self.dialogs) > 1:
                        self.dialogs.pop(0)
                    else:
                        dialogManager.start(self.myMap, *self.dialogs[0][1:])
                        self.startJumpTime = time()
                        self.actions.pop(0)
            else:
                if self.nextDialogTime[1] <= 0:
                    self.nextDialogTime = [time(), self.dialogs[0][0][0]]
                    dialogManager.start(self.myMap, *self.dialogs[0][1:])
                    print("mmm")
                else:
                    self.nextDialogTime[1] -= time() - self.nextDialogTime[0]
                    self.nextDialogTime[0] = time()
                if self.nextDialogTime[1] <= 0:
                    print('how')
                    self.dialogs[0][0][1]()
                    self.dialogs.pop(0)
                    self.actions.pop(0)

        def actionsPlay(self):
            self.actions[0]()

    class Story2:
        def reset(self):
            try:
                self.myMap.clear()
            except:
                pass

        def start(self):
            self.nextDialogTime = [time(), 0]
            game.setMap('дом 2')
            self.myMap = game.getMap('дом 2')
            self.reset()
            self.myMap.resize(*homeFirstSize)

            self.oldManPos = (.72, .6)
            self.heroPos = (.63, .63)
            mapW, mapH = self.myMap.w, self.myMap.h
            self.oldMan = Image('images/old-man-sitting.png', mapW*self.oldManPos[0], mapH*self.oldManPos[1], 100, 100)
            self.hero = Image('images/hero.png', mapW*self.heroPos[0], mapH*self.heroPos[1], 90, 90)

            self.currentDialog = -1
            self.dialogs = [
                [(14.6, None), 'Я прочитал эту книгу и там было написано про какойто затерянный город с богатствами, нам обязательно нужно его найти. Только отправимся завтра, ато спать охота', .08, 1, 'old-man-cut0.png'],
                ]
            self.heroImages = [1, 1, 2]
            
            self.myMap.addElement([self.oldMan, self.hero])
            self.myMap.eventHandler.onLoopUpdate.addElement(self.onResize)
            self.myMap.eventHandler.onLoopUpdate.addElement(self.dialogAutoUpdate)
            self.myMap.eventHandler.onClick.addElement(self.myMap, self.nextDialog)

        def nextDialog(self, *args):
            self.currentDialog += 1
            if len(self.dialogs) > self.currentDialog:
                self.nextDialogTime = [time(), self.dialogs[self.currentDialog][0][0]]
                if self.dialogs[self.currentDialog][0][1]:
                    self.dialogs[self.currentDialog][0][1]()
                dialogManager.start(self.myMap, *self.dialogs[self.currentDialog][1:])
            else:
                dialogManager.stop()
                self.myMap.eventHandler.onClick.delElement(self.myMap)
                self.myMap.eventHandler.onLoopUpdate.delElement(self.dialogAutoUpdate)
                darkScreenAnimation.newStory(gameStory.Story3())
                setLvl(3)

        def dialogAutoUpdate(self):
            self.nextDialogTime[1] -= time() - self.nextDialogTime[0]
            self.nextDialogTime[0] = time()
            if self.nextDialogTime[1] <= 0:
                self.nextDialog()

        def onResize(self, *args):
            w, h = sc.get_size()
            if (self.myMap.w != w) & (self.myMap.h != h):
                multiplier = setMaxScreenSizeToElement(self.myMap)
                mapW, mapH = self.myMap.w, self.myMap.h

                self.oldMan.resize(self.oldMan.w*multiplier, self.oldMan.h*multiplier)
                self.oldMan.setPos(mapW*self.oldManPos[0], mapH*self.oldManPos[1])

                self.hero.resize(self.hero.w*multiplier, self.hero.h*multiplier)
                self.hero.setPos(mapW*self.heroPos[0], mapH*self.heroPos[1])

    class Story3:
        def reset(self):
            try:
                self.myMap.clear()
            except:
                pass

        def start(self):
            self.nextDialogTime = [time(), 0]
            game.setMap('улица')
            self.myMap = game.getMap('улица')
            self.reset()
            self.myMap.resize(*streetFirstSize)

            self.oldManPos = (.51, .6)
            self.heroPos = [.66, .65]
            mapW, mapH = self.myMap.w, self.myMap.h
            self.oldMan = Image('images/old-man.png', mapW*self.oldManPos[0], mapH*self.oldManPos[1], 70, 70)
            self.hero = Image(['images/hero2.png', 'images/hero.png'], mapW*self.heroPos[0], mapH*self.heroPos[1], 63, 63)

            self.currentDialog = -1
            self.dialogs = [
                [(3.6, None), 'Какой прекрасный день', .08, 1, 'old-man-cut0.png'],
                [(9, None), 'Чего встал ? Думал я с тобой поплыву ? Неет я для этого уже стар, оправляйся ка ты один', .08, 1, 'old-man-cut0.png'],
                [(3, None), 'Ааа.. ээээ.. ну ладно', .08, 1, 'hero-cut0.png'],
                [(3, lambda: self.myMap.eventHandler.onLoopUpdate.addElement(self.mooveRight)), 'Ааа.. ээээ.. ну ладно', .01, -10, 'hero-cut0.png'],
                [(0, self.stopMooveRight), 'Ааа.. ээээ.. ну ладно', .01, -10, 'hero-cut0.png'],
                ]
            self.heroImages = [1, 1, 2]
            
            self.myMap.addElement([self.oldMan, self.hero])
            self.myMap.eventHandler.onLoopUpdate.addElement(self.onResize)
            self.myMap.eventHandler.onLoopUpdate.addElement(self.dialogAutoUpdate)
            self.myMap.eventHandler.onClick.addElement(self.myMap, self.nextDialog)

        def mooveRight(self):
            self.hero.changeImage(1)
            mapW, mapH = self.myMap.w, self.myMap.h
            self.heroPos[0] += .002
            self.hero.setPos(mapW*self.heroPos[0], mapH*self.heroPos[1])

        def stopMooveRight(self):
            self.hero.changeImage(1)
            self.myMap.eventHandler.onLoopUpdate.delElement(self.mooveRight)

        def nextDialog(self, *args):
            self.currentDialog += 1
            if len(self.dialogs) > self.currentDialog:
                self.nextDialogTime = [time(), self.dialogs[self.currentDialog][0][0]]
                if self.dialogs[self.currentDialog][0][1]:
                    self.dialogs[self.currentDialog][0][1]()
                dialogManager.start(self.myMap, *self.dialogs[self.currentDialog][1:])
            else:
                dialogManager.stop()
                self.myMap.eventHandler.onClick.delElement(self.myMap)
                self.myMap.eventHandler.onLoopUpdate.delElement(self.dialogAutoUpdate)
                darkScreenAnimation.newStory(gameStory.Story4())
                setLvl(4)

        def dialogAutoUpdate(self):
            self.nextDialogTime[1] -= time() - self.nextDialogTime[0]
            self.nextDialogTime[0] = time()
            if self.nextDialogTime[1] <= 0:
                self.nextDialog()

        def onResize(self, *args):
            w, h = sc.get_size()
            if (self.myMap.w != w) & (self.myMap.h != h):
                multiplier = setMaxScreenSizeToElement(self.myMap)
                mapW, mapH = self.myMap.w, self.myMap.h

                self.oldMan.resize(self.oldMan.w*multiplier, self.oldMan.h*multiplier)
                self.oldMan.setPos(mapW*self.oldManPos[0], mapH*self.oldManPos[1])

                self.hero.resize(self.hero.w*multiplier, self.hero.h*multiplier)
                self.hero.setPos(mapW*self.heroPos[0], mapH*self.heroPos[1])

    class Story4:
        def reset(self):
            try:
                self.myMap.clear()
            except:
                pass

        def start(self):
            self.nextDialogTime = [time(), 0]
            game.setMap('вода 1')
            self.myMap = game.getMap('вода 1')
            self.reset()
            self.myMap.addElement(waterRect1)
            self.heroPos = (.66, .63)
            self.temple = Image('images/temple.png', 2900, self.myMap.h - 180 ,180, 180)
            self.hero = Image(['images/hero.png', 'images/hero1.png', *[f'images/hero-jump{i}.png' for i in range(11)], 'images/hero4.png'], 300, 186, 90, 90)
            self.boat = Image(['images/boat.png'], 260, 160, 160, 160)
            self.sand = Image('images/sand.png', -1000, self.myMap.h, self.myMap.w + 2000, 800)
            self.templeHoverText = Button("Войти ?  :}", self.temple.x, self.temple.y + 40, fontSize=26)
            self.jumpTime = .06
            self.heroMooveY = 1
            self.respawn = None
            self.lines = []
            for i in range(4):
                self.lines.append([])
                for j in range((self.myMap.w) // 200):
                    self.lines[-1].append(selfRect(50 + j*200 + randint(-50, 50), 300 + 230*i + randint(-50, 50), 10, 2, (240, 240, 240)))
                    self.myMap.addElement(self.lines[-1][-1])

            self.currentDialog = -1
            self.dialogs = [
                [(5, lambda: self.myMap.eventHandler.onLoopUpdate.addElement(self.mooveRight)), '(Мдаа и что нашло на этого страрика)', .08, 1, 'hero-cut0.png'],
                [(4, None), 'Похоже приплыл', .08, 1, 'hero-cut0.png'],
                [(5, None), 'Так, мне надо найти храм', .08, 1, 'hero-cut0.png'],
                ]

            self.actions = [self.nextDialog, self.nextDialog, self.nextDialog, self.stopDialog, self.startJumpToWater, self.jumpToWater, self.moove]
            self.myMap.addElement([self.hero, self.boat, self.sand])
            self.myMap.eventHandler.onLoopUpdate.addElement(self.actionsPlay)
            self.myMap.eventHandler.mouseHover.addElement(self.temple, self.showTempleText, self.hideTempleText)
            self.myMap.eventHandler.onClick.addElement(self.temple, self.openTemple)
            self.myMap.eventHandler.onClick.addElement(self.myMap, self.resetDialogTime)
            self.spawnDecor()

        def spawnDecor(self):
            try:
                for i in self.fish:
                    if i[1][0] > i[0].x:
                        i[0].moove(1)
                        if i[2]: i[0].flip(); i[2] = False
                    elif i[1][0] == i[0].x:
                        pass
                    else:
                        i[0].moove(-1)
                        if not i[2]: i[0].flip(); i[2] = True
                    if i[1][1] > i[0].y:
                        i[0].moove(y=1)
                    elif i[1][1] == i[0].y:
                        pass
                    else:
                        i[0].moove(y=-1)   
                    if (i[0].x == i[1][0]) & (i[0].y == i[1][1]):
                        i[1] = [int(randint(50, self.myMap.w - 100)), int(randint(500, self.myMap.h - 100))]
            except:
                self.decor = []
                for i in range(5):
                    size = randint(300, 800)
                    self.decor.append(Image(f'images/stone{randint(0, 1)}.png', randint(100, self.myMap.w - 70), self.myMap.h-size/2, size, size/2))
                    while self.decor[-1].collideobjects(self.decor[:-1]):
                        self.decor[-1].setPos(randint(100, self.myMap.w - 70))
                    self.myMap.addElement(self.decor[-1])
                self.fish = []
                self.myMap.addElement(self.temple)
                for i in range(20):
                    size = randint(30, 50)
                    self.decor.append(Image(f'images/leaves{randint(0, 3)}.png', randint(100, self.myMap.w - 70), self.myMap.h-size, size, size))
                    self.myMap.addElement(self.decor[-1])
                for i in range(14):
                    pos = [int(randint(50, self.myMap.w - 100)), int(randint(500, self.myMap.h - 100))]
                    pos2 = [int(randint(50, self.myMap.w - 100)), int(randint(500, self.myMap.h - 100))]
                    self.fish.append([Image(f'images/fish{randint(0, 7)}.png', *pos, 30, 30), pos2, False])
                    self.myMap.addElement(self.fish[-1][0])
                self.myMap.eventHandler.onLoopUpdate.addElement(self.spawnDecor)

        def borderRespawn(self):
            if self.respawn == None:
                self.respawn = time() + .6
            try:
                for i in self.mermaid[:4]:
                    i.moove(4)
                for i in self.mermaid[4:]:
                    i.moove(-4)

            except:
                self.mermaid = []
                x = -600
                for i in range(4):
                    self.mermaid.append(Image('images/mermaid.png', x, 300 + 220 * i, 130, 130))
                x = self.myMap.w + 600
                for i in range(4):
                    self.mermaid.append(Image('images/mermaid.png', x, 300 + 220 * i, 130, 130))
                self.myMap.addElement(self.mermaid)

        def openTemple(self, *args):
            darkScreenAnimation.newStory(gameStory.Story5())
            setLvl(5)

        def showTempleText(self, *args):
            self.myMap.addElement(self.templeHoverText)
            
        def hideTempleText(self, *args):
            self.myMap.delElement(self.templeHoverText)

        def resetDialogTime(self, *args):
            self.nextDialogTime[1] = .001

        def startJumpToWater(self):
            self.startJumpTime = time()
            self.actions.pop(0)

        def jumpToWater(self):
            if (self.hero.imgIndex < 12):
                if self.jumpTime <= time() - self.startJumpTime:
                    self.startJumpTime = time()
                    self.hero.changeImage(self.hero.imgIndex+1)

            if self.hero.x < 650:
                self.hero.moove(3, -1)
            elif self.hero.y >= self.myMap.h - self.hero.h:
                self.actions.pop(0)
                dialogManager.stop()
                self.hero.changeImage(1)
            else:
                self.heroMooveY += .06
                if self.heroMooveY > 5:
                    self.heroMooveY = 5
                self.hero.moove(1, self.heroMooveY)
                w, h = sc.get_size()
                if self.hero.y > h/2 - self.hero.h/2:
                    self.myMap.anchorCameraAtElement(self.hero)

        def mooveRight(self):
            if self.hero.x < 550:
                self.hero.moove(1)
                self.boat.moove(1)
            else:
                self.hero.changeImage(1)
                self.myMap.eventHandler.onLoopUpdate.delElement(self.mooveRight)

        def nextDialog(self, *args):  
            if len(self.dialogs) > 0:
                if self.nextDialogTime[1] <= 0:
                    self.nextDialogTime = [time(), self.dialogs[0][0][0]]
                    dialogManager.start(self.myMap, *self.dialogs[0][1:])
                    if self.dialogs[0][0][1]:
                        self.dialogs[0][0][1]()
                else:
                    self.nextDialogTime[1] -= time() - self.nextDialogTime[0]
                    self.nextDialogTime[0] = time()
            if self.nextDialogTime[1] <= 0:
                if len(self.dialogs) > 0:
                    self.dialogs.pop(0)
                    self.actions.pop(0)

        def stopDialog(self):
            dialogManager.stop()
            self.actions.pop(0)

        def moove(self):
            if (self.hero.x < 0) or (self.hero.x > self.myMap.w):
                self.borderRespawn()
            if self.respawn != None:
                if type(self.respawn) == str:
                    pass
                else:
                    if time() > self.respawn:
                        if difficultSetting.actionAfterDie == 'respawn':
                            darkScreenAnimation.newStory(gameStory.Story4())
                        else:
                            darkScreenAnimation.newStory(gameStory.Story0())
                        self.respawn = "a"
            if dialogManager.work: dialogManager.stop()
            keys.updateKeys()
            speed = 3
            x, y = [(-keys.a + keys.d) * speed, (-keys.w + keys.s) * speed]
            if y == 0:
                y = 1
            if x >= 1: self.hero.changeImage(1)
            if x <= 1: self.hero.changeImage(13)
            self.hero.moove(x, y)
            if self.hero.y > self.myMap.h - self.hero.h: self.hero.setPos(y=self.myMap.h - self.hero.h)
            if self.hero.y < 500: self.hero.setPos(y=500)

        def actionsPlay(self):
            self.actions[0]()

    class Story5:
        def reset(self):
            try:
                self.myMap.clear()
            except:
                pass

        def start(self):
            self.nextDialogTime = [time(), 0]
            game.setMap('храм вход')
            self.myMap = game.getMap('храм вход')
            self.reset()
            
            self.gate = Image(['images/gate2.png', 'images/gate1.png', 'images/gate0.png'], 100, 100, 200, 280)
            self.neptune = Image('images/neptune.png', 100, 100, 68*3, 68*3)
            self.myMap.addElement(self.gate)

            self.currentDialog = -1
            self.dialogs = [
                [(7, None), 'Чтоо, что бы войти внутрь надо собрать мозайку ?', .06, 2, 'hero-cut2.png'],
                [(4, None), 'Да да именно так, нужно кусочки от мозайки ставить на голубые квадратики', .05, 1, 'robot.png'],
                [(4, None), 'Уф, наконец собрал', .05, 1, 'hero-cut2.png'],
                [(2, self.nextGateImage), 'Уф, наконец собрал', .05, 1, 'hero-cut2.png'],
                [(1, self.nextGateImage), 'Уф, наконец собрал', .001, -10, 'hero-cut2.png'],
                [(.6, None), 'Уф, наконец собрал', .001, -10, 'hero-cut2.png'],
                ]

            self.mazeRects = []
            self.mazeImages = []
            self.mazePos = (0, 0)
            for i in range(3):
                self.mazeRects.append([])
                self.mazeImages.append([])
                for j in range(3):
                    self.mazeImages[-1].append(Image(f"images/neptune{3*i +(j+1)}.png", self.mazePos[0] + 600 + randint(0, 160), self.mazePos[1] + 200 + randint(0, 160), 62, 62))
                    self.mazeRects[-1].append(selfRect(self.mazePos[0]-2 + 66*j, self.mazePos[1]-2 + 66*i, 66, 66, (30, 30, 150)))
                self.myMap.addElement(self.mazeRects[-1])
            for i in range(3):
                self.myMap.addElement(self.mazeImages[i])
            self.catchedImage = None

            self.actions = [self.nextDialog, self.nextDialog, self.mooveMaze, self.nextDialog, self.nextDialog, self.nextDialog, self.nextDialog, self.nextStory]
            self.myMap.eventHandler.onClick.addElement(self.myMap, self.resetDialogTime)
            self.myMap.eventHandler.onLoopUpdate.addElement(self.onResize)
            self.myMap.eventHandler.onLoopUpdate.addElement(self.actionsPlay)

            self.lines = []
            for i in range(4):
                self.lines.append([])
                for j in range((self.myMap.w) // 200):
                    self.lines[-1].append(selfRect(50 + j*200 + randint(-50, 50), 300 + 230*i + randint(-50, 50), 10, 2, (240, 240, 240)))
                    self.myMap.addElement(self.lines[-1][-1])
            self.myMap.addElement(Image('images/waterRect.png', 0, 0, 3000, 3000))

        def nextGateImage(self):
            self.gate.changeImage(self.gate.imgIndex + 1)

        def nextStory(self):
            darkScreenAnimation.newStory(gameStory.Story6())
            self.actions.pop(0)
            setLvl(6)

        def mooveMaze(self):
            pressed = pg.mouse.get_pressed()[0]
            x, y = getMousePos()
            plasedMaze = 0
            sixAndNineRects = [self.mazeRects[1][2], self.mazeRects[2][2]]
            if not(self.catchedImage and pressed):
                self.catchedImage = None
                for i in range(2, -1, -1):
                    for j in range(2, -1, -1):
                        if isMouseRectCollide(self.mazeImages[i][j]):
                            if not self.catchedImage:
                                if pressed:
                                    self.catchedImage = self.mazeImages[i][j]

            if self.catchedImage:
                self.catchedImage.setPos(x-10, y-10)
            else:
                for i in range(3):
                    for j in range(3):
                        if (j == 2) and ((i == 1) or (i == 2)):
                            for k in sixAndNineRects:
                                if k.x + 15 > self.mazeImages[i][j].x > k.x - 15:
                                    if k.y + 15 > self.mazeImages[i][j].y > k.y - 15:
                                        plasedMaze += 1
                                        sixAndNineRects.remove(k)
                        else:
                            if self.mazeRects[i][j].x + 15 > self.mazeImages[i][j].x > self.mazeRects[i][j].x - 15:
                                if self.mazeRects[i][j].y + 15 > self.mazeImages[i][j].y > self.mazeRects[i][j].y - 15:
                                    plasedMaze += 1
                if plasedMaze == 9:
                    self.complitePuzzle()

        def complitePuzzle(self):
            for i in range(3):
                for j in range(3):
                    self.myMap.delElement(self.mazeImages[i][j])
                    self.myMap.delElement(self.mazeRects[i][j])
            self.myMap.addElement(self.neptune)
            self.nextDialogTime = [time(), 0]
            self.actions.pop(0)

        def resetDialogTime(self, *args):
            self.nextDialogTime[1] = .001
        
        def nextDialog(self, *args):
            if len(self.dialogs) > 0:
                if self.nextDialogTime[1] <= 0:
                    self.nextDialogTime = [time(), self.dialogs[0][0][0]]
                    dialogManager.start(self.myMap, *self.dialogs[0][1:])
                    if self.dialogs[0][0][1]:
                        self.dialogs[0][0][1]()
                else:
                    self.nextDialogTime[1] -= time() - self.nextDialogTime[0]
                    self.nextDialogTime[0] = time()
            if self.nextDialogTime[1] <= 0:
                if len(self.dialogs) > 0:
                    self.dialogs.pop(0)
                    self.actions.pop(0)

        def stopDialog(self):
            dialogManager.stop()
            self.actions.pop(0)

        def actionsPlay(self):
            if len(self.actions) > 0:
                self.actions[0]()

        def onResize(self, *args):
            w, h = sc.get_size()
            if (self.myMap.w != w) | (self.myMap.h != h):
                self.myMap.resize(w, h)
                
                self.mazePos = [300, h/2 - 160]
                self.gate.setPos(self.mazePos[0] - 200, h/2 - 160)
                self.neptune.setPos(*self.mazePos)
                for i in range(3):
                    for j in range(3):
                        self.mazeRects[i][j].setPos(self.mazePos[0]-2 + 68*j, self.mazePos[1]-2 + 68*i)

    class Story6:
        def reset(self):
            try:
                self.myMap.clear()
            except:
                pass

        def start(self):
            w, h = sc.get_size()
            self.gameH = 600
            self.nextDialogTime = [time(), 0]
            game.setMap('дорога со стрелами')
            self.myMap = game.getMap('дорога со стрелами')
            self.reset()
            self.newMarlinTimeOut = randint(1, 3)
            self.newMarlinStartTime = time()
            self.marlins = []
            self.funText = [Button("Смотри как пляшет", 1800, 120, fontSize=20), Button("каждый раз смеюсь с этого", 1760, 150, fontSize=20)]
            self.drawFunText = False
            self.stoneWall = Image('images/stone-wall3.png', -120, self.gameH, 2160, 600)


            self.pathImgs = [Image("images/stone-wall2.png", 0 + 960*i, 0, 960, self.gameH) for i in range(2)]
            self.hero = Image('images/hero3.png', 200, 200, 25, 50)
            self.heroY = 200
            self.towers = [Image("images/tower2.png", 1820, 100 + 300*i, 120, 100) for i in range(2)]
            self.gates = [Image('images/gate3.png', 1920, 0, 120, self.gameH), Image('images/gate4.png', -120, 0, 120, self.gameH)]

            self.dialogs = [
                [(6, None), 'Что то не хорошее у меня предчуствие', .03, 2, 'hero-cut2.png'],
                [(6, None), '(хах) Явился не запылился, спустить марлинов!!!', .03, .3, 'mermaid.png'],
                [(1, None), 'Чтоо ?', .02, .01, 'hero-cut2.png'],
                [(2.5, None), 'Наконеец', .02, .01, 'hero-cut2.png'],
                ]

            self.actions = [self.nextDialog, self.nextDialog, self.nextDialog, self.stopDialog, self.moove, self.newStory]
            self.myMap.addElement([*self.pathImgs, self.stoneWall, *self.towers, *self.gates, self.hero])
            self.myMap.eventHandler.onClick.addElement(self.myMap, self.resetDialogTime)
            self.myMap.eventHandler.onLoopUpdate.addElement(self.actionsPlay)

        def newStory(self):
            darkScreenAnimation.newStory(gameStory.Story7())
            self.actions.pop(0)
            setLvl(7)

        def spawnMarlins(self):
            for i in self.marlins:
                if self.hero.colliderect(i):
                    self.heroY = 200
                    self.hero.setPos(200, 200)
                i.moove(-5)
                if not(self.hero.y - 30 < i.y < self.hero.y + self.hero.h - 20):
                    i.moove(y=2 if i.y < self.hero.y + self.hero.h - 20 else -2)
                if i.x < -120:
                    self.myMap.delElement(i)
                    self.marlins.remove(i)
            self.newMarlinTimeOut -= time() - self.newMarlinStartTime
            self.newMarlinStartTime = time()
            if self.newMarlinTimeOut <= 0:
                self.newMarlinTimeOut = 1.8
                self.marlins.append(Image('images/marlin.png', 2040, 40 + randint(0, 10)*48, 100, 50))
                self.myMap.addElement(self.marlins[-1])
            if self.hero.collideobjects(self.marlins):
                playSound('marlin-hit')
                if difficultSetting.actionAfterDie == 'respawn':
                    darkScreenAnimation.newStory(gameStory.Story6())
                else:
                    darkScreenAnimation.newStory(gameStory.Story0())

        def moove(self):
            w, h = sc.get_size()
            if dialogManager.work: dialogManager.stop()
            keys.updateKeys(); speed = 3
            x, y = [(-keys.a + keys.d) * difficultSetting.selfSpeedInArrowMap, (-keys.w + keys.s) * 3.7]
            self.heroY += y
            self.hero.moove(x)
            if self.hero.collideobjects(self.towers): self.hero.moove(-x)
            self.hero.setPos(y=self.heroY)
            if self.hero.collideobjects(self.towers): self.heroY -= y; self.hero.setPos(y=self.heroY)
            if self.hero.x < 0: self.hero.setPos(0)
            if self.hero.y < 0: self.hero.setPos(y=0); self.heroY=0
            elif self.hero.y > self.gameH - self.hero.h: self.heroY=self.gameH - self.hero.h; self.hero.setPos(y=self.heroY)
            mapX = self.hero.x - 200
            if mapX > 1920 - w + 120: mapX = 1920 - w + 120
            elif mapX < -120: mapX = -120

            if not self.drawFunText:
                if self.hero.x > 2160 - w:
                    self.drawFunText = True
                    self.myMap.addElement(self.funText)

            self.myMap.x = -mapX
            if self.hero.colliderect(self.gates[0]):
                self.actions.pop(0)

        def resetDialogTime(self, *args):
            self.nextDialogTime[1] = .001
        
        def nextDialog(self, *args):
            if len(self.dialogs) > 0:
                if self.nextDialogTime[1] <= 0:
                    self.nextDialogTime = [time(), self.dialogs[0][0][0]]
                    dialogManager.start(self.myMap, *self.dialogs[0][1:])
                    if self.dialogs[0][0][1]:
                        self.dialogs[0][0][1]()
                else:
                    self.nextDialogTime[1] -= time() - self.nextDialogTime[0]
                    self.nextDialogTime[0] = time()
            if self.nextDialogTime[1] <= 0:
                if len(self.dialogs) > 0:
                    self.dialogs.pop(0)
                    self.actions.pop(0)

        def stopDialog(self):
            dialogManager.stop()
            self.actions.pop(0)
            self.myMap.eventHandler.onLoopUpdate.addElement(self.spawnMarlins)

        def actionsPlay(self):
            if len(self.actions) > 0:
                self.actions[0]()

        def onResize(self, *args):
            w, h = sc.get_size()
            if (self.myMap.w != w) | (self.myMap.h != h):
                self.myMap.resize(w, h)
                
                self.mazePos = [300, h/2 - 160]
                self.gate.setPos(self.mazePos[0] - 200, h/2 - 160)
                self.neptune.setPos(*self.mazePos)
                for i in range(3):
                    for j in range(3):
                        self.mazeRects[i][j].setPos(self.mazePos[0]-2 + 68*j, self.mazePos[1]-2 + 68*i)

    class Story7:
        def reset(self):
            try:
                self.myMap.clear()
            except:
                pass

        def start(self):
            w, h = sc.get_size()
            self.gameH = 600
            self.nextDialogTime = [time(), 0]
            game.setMap('лабиринт')
            self.myMap = game.getMap('лабиринт')
            self.reset()
            
            self.floor = Image("images/stone-wall2.png", 0, 0, 400 + 300*6 + 20, 300*6 + 20)
            self.carpet = Image('images/carpet.png', 400 + 300*6 - 200, 300*6 - 160, 140, 140)
            mazePos = [400, 0]
            length = 300
            mazeData = [
                [-2, 1, 2, 20],
                [0, 1, 20, 5],
                [0, 6, 5, 20],
                [0, 0, 6, 20],
                [6, 0, 20, 6],
                [5, 0, 20, 2],
                [4, 1, 20, 2],
                [4, 3, 2, 20],
                [0, 2, 2, 20],
                [1, 2, 20, 1],
                [1, 1, 2, 20],
                [3, 1, 20, 4],
                [2, 3, 1, 20],
                [1, 5, 2, 20],
                [0, 4, 5, 20],
                [4, 5, 1, 20],
                [4, 5, 20, 1],
            ]
            self.maze = []
            for i in mazeData:
                data = [i[0] * length + mazePos[0], i[1] * length + mazePos[1], i[2], i[3]]
                if data[2] == 20:
                    data[3] *= length
                else:
                    data[2] *= length
                self.maze.append(selfRect(*data, (20, 20, 20)))
            self.hero = Image('images/hero3.png', 100, 100, 25, 50)

            self.dialogs = [
                [(4, None), 'Уф, еле прошёл', .03, 2, 'hero-cut2.png'],
                [(3.6, None), 'Так а это похоже лабиринт', .03, .3, 'hero-cut2.png'],
                ]

            self.actions = [self.nextDialog, self.nextDialog, self.stopDialog, self.moove, self.newStory]
            self.myMap.addElement([self.floor, *self.maze, self.carpet, self.hero])
            self.myMap.eventHandler.onClick.addElement(self.myMap, self.resetDialogTime)
            self.myMap.eventHandler.onLoopUpdate.addElement(self.actionsPlay)

        def newStory(self):
            darkScreenAnimation.newStory(gameStory.Story8())
            self.actions.pop(0)
            setLvl(8)

        def moove(self):
            w, h = sc.get_size()
            if dialogManager.work: dialogManager.stop()
            keys.updateKeys(); speed = 4
            x, y = [(-keys.a + keys.d) * speed, (-keys.w + keys.s) * speed]
            self.hero.moove(x)
            if self.hero.collideobjects(self.maze):
                self.hero.moove(-x)
            self.hero.moove(y=y)
            if self.hero.collideobjects(self.maze):
                self.hero.moove(y=-y)

            mapPos = [self.hero.x - w/2, self.hero.y - h/2]
            if mapPos[0] < 0: mapPos[0] = 0
            elif self.hero.x > self.floor.w - w/2: mapPos[0] = self.floor.w - w
            if mapPos[1] < 0: mapPos[1] = 0
            elif self.hero.y > self.floor.h - h/2: mapPos[1] = self.floor.h - h
            if self.hero.colliderect(self.carpet):
                self.actions.pop(0)
            self.myMap.x = -mapPos[0]; self.myMap.y = -mapPos[1]
            if self.hero.x < 0:
                self.hero.setPos(0)
            elif self.hero.x > self.myMap.w - self.hero.w:
                self.hero.setPos(self.myMap.w - self.hero.w)
            if self.hero.y < 0:
                self.hero.setPos(y=0)
            elif self.hero.y > self.myMap.h - self.hero.h*5:
                self.hero.setPos(y=self.myMap.h - self.hero.h*5)
            
        def resetDialogTime(self, *args):
            self.nextDialogTime[1] = .001
        
        def nextDialog(self, *args):
            if len(self.dialogs) > 0:
                if self.nextDialogTime[1] <= 0:
                    self.nextDialogTime = [time(), self.dialogs[0][0][0]]
                    dialogManager.start(self.myMap, *self.dialogs[0][1:])
                    if self.dialogs[0][0][1]:
                        self.dialogs[0][0][1]()
                else:
                    self.nextDialogTime[1] -= time() - self.nextDialogTime[0]
                    self.nextDialogTime[0] = time()
            if self.nextDialogTime[1] <= 0:
                if len(self.dialogs) > 0:
                    self.dialogs.pop(0)
                    self.actions.pop(0)

        def stopDialog(self):
            dialogManager.stop()
            self.actions.pop(0)

        def actionsPlay(self):
            if len(self.actions) > 0:
                self.actions[0]()

    class Story8:
        def reset(self):
            try:
                self.myMap.clear()
            except:
                pass

        def start(self):
            w, h = sc.get_size()
            self.gameH = 600
            self.nextDialogTime = [time(), 0]
            game.setMap('босс')
            self.myMap = game.getMap('босс')
            self.reset()
            self.spawnTimeStart = 1
            self.tornadoTimeImage = .5
            
            self.hero = Image('images/hero3.png', 100, 300, 25, 50)
            self.neptune = Image('images/neptune-fight.png', w/2, h/2, 100, 60)
            self.marline = []
            self.marline2 = []
            self.marlineSpawnTime = time() + 2
            self.marlineSpawnTime2 = time() + 2
            self.tornado = []
            self.mirrirSpawn = time() + 2
            self.mirrorFish = []
            self.respawn = False
            self.dialogs = [
                [(7.6, None), 'А вот и ты, раньше чем я ожидал. Хвалю, Удивишь ли ты меня так же в сражении ?', .05, 2, 'neptune-cut.png'],
                [(8.2, None), '(Ёмае, куда я забрел.. я же просто хотел найти сокровища, а тут еще эта рыба драки хочет)', .05, .3, 'hero-cut2.png'],
                [(3.6, self.setFirstSpawnTime), 'А я обязательно должен сражаться ?', .03, .3, 'hero-cut2.png'],
                ]

            self.actions = [self.nextDialog, self.nextDialog, self.nextDialog, self.stopDialog, self.moove]
            self.myMap.addElement([self.neptune, self.hero])
            self.myMap.eventHandler.onClick.addElement(self.myMap, self.resetDialogTime)
            self.myMap.eventHandler.onLoopUpdate.addElement(self.actionsPlay)
            self.myMap.eventHandler.onLoopUpdate.addElement(self.onResize)

        # устанавливает время когда станут появляется первые предметы
        def setFirstSpawnTime(self):
            self.marlineSpawnTime = time() + 1
            self.marlineSpawnTime2 = time() + difficultSetting.marlinWaitSpawnBos
            self.mirrirSpawn = time() + difficultSetting.mirrorFishWaitSpawn


        # спавнит предметы, двигает их, проверяет столкновения
        def mobsEngine(self):
            w, h = sc.get_size()
            if time() - self.spawnTimeStart > difficultSetting.tornadoSpawnSpeed:
                playSound('storm')
                self.spawnTimeStart = time()
                angle = getAngle((w/2 + 10, h/2), (w/2, h/2), (self.hero.x, self.hero.y))
                self.tornado.append([Image(['images/tornado0.png', 'images/tornado1.png'], w/2, h/2, 60, 60), angle, [w/2, h/2], False])
                self.myMap.addElement(self.tornado[-1][0])
            if time() - self.marlineSpawnTime > difficultSetting.marlinSpeedSpawnBos:
                self.marlineSpawnTime = time()
                self.marline.append(Image('images/marlin.png', w, self.hero.y + 10, 100, 50))
                self.myMap.addElement(self.marline[-1])
            if time() - self.marlineSpawnTime2 > 1 + difficultSetting.marlinSpeedSpawnBos:
                self.marlineSpawnTime2 = time()
                self.marline2.append(Image('images/marlin2.png', -100, self.hero.y + 10, 100, 50))
                self.myMap.addElement(self.marline2[-1])
            if time() - self.tornadoTimeImage > .1:
                self.tornadoTimeImage = time()
                for i in self.tornado:
                    i[0].changeImage(0 if i[0].imgIndex else 1)
            if time() - self.mirrirSpawn > difficultSetting.mirrorFishRespawnBos:
                self.mirrirSpawn = time()
                self.mirrorFish.append(Image('images/mirror-fish.png', w*.2, - 100, 40, 80))
                self.myMap.addElement(self.mirrorFish[-1])
            for i in self.tornado:
                for j in self.mirrorFish:
                    if i[0].colliderect(j):
                        angle = getAngle((j.x + 10, j.y), (j.x, j.y), (w/2, h/2 + 10))
                        i[1] = angle
                        i[3] = True

                i[2][0] += cos(radians(i[1]))*4
                i[2][1] += sin(radians(i[1]))*4
                i[0].setPos(*i[2])
                if i[3] == True:
                    if i[0].colliderect(self.neptune):
                        darkScreenAnimation.newStory(gameStory.Story9())
                        setLvl(9)
                        self.actions.pop(0)
                if (i[0].x < -70) or (i[0].x > w) or (i[0].y < -70) or (i[0].y > h):
                    self.myMap.delElement(i[0])
                    self.tornado.remove(i)

            for i in self.marline:
                i.moove(-5)
                if i.x > w:
                    self.myMap.delElement(i)
                    self.marline.remove(i)

            for i in self.marline2:
                i.moove(5)
                if i.x > w:
                    self.myMap.delElement(i)
                    self.marline2.remove(i)
            for i in self.mirrorFish:
                i.moove(y=3)
                if i.y > h:
                    self.myMap.delElement(i)
                    self.mirrorFish.remove(i)

            for i in self.tornado:
                if i[0].colliderect(self.hero):
                    if not self.respawn:
                        if difficultSetting.actionAfterDie == 'respawn':
                            darkScreenAnimation.newStory(gameStory.Story8())
                        else:
                            darkScreenAnimation.newStory(gameStory.Story0())
                        self.respawn = True

            if self.hero.collideobjects(self.marline) or self.hero.collideobjects(self.marline2):
                playSound('marlin-hit')
                if not self.respawn:
                    if difficultSetting.actionAfterDie == 'respawn':
                        darkScreenAnimation.newStory(gameStory.Story8())
                    else:
                        darkScreenAnimation.newStory(gameStory.Story0())
                    self.reset = True

        # движение героя
        def moove(self):
            w, h = sc.get_size()
            self.mobsEngine()
            if dialogManager.work: dialogManager.stop()
            keys.updateKeys(); speed = 4
            x, y = [(-keys.a + keys.d) * speed, (-keys.w + keys.s) * speed]
            self.hero.moove(x)
            self.hero.moove(y=y)
            if self.hero.x < 0:
                self.hero.setPos(0)
            elif self.hero.x > w - self.hero.w:
                self.hero.setPos(w - self.hero.w)
            if self.hero.y < 0:
                self.hero.setPos(y=0)
            elif self.hero.y > h - self.hero.h:
                self.hero.setPos(y=h - self.hero.h)
   
        def resetDialogTime(self, *args):
            self.nextDialogTime[1] = .001
        
        def nextDialog(self, *args):
            if len(self.dialogs) > 0:
                if self.nextDialogTime[1] <= 0:
                    self.nextDialogTime = [time(), self.dialogs[0][0][0]]
                    dialogManager.start(self.myMap, *self.dialogs[0][1:])
                    if self.dialogs[0][0][1]:
                        self.dialogs[0][0][1]()
                else:
                    self.nextDialogTime[1] -= time() - self.nextDialogTime[0]
                    self.nextDialogTime[0] = time()
            if self.nextDialogTime[1] <= 0:
                if len(self.dialogs) > 0:
                    self.dialogs.pop(0)
                    self.actions.pop(0)

        def stopDialog(self):
            dialogManager.stop()
            self.actions.pop(0)

        def actionsPlay(self):
            if len(self.actions) > 0:
                self.actions[0]()

        def onResize(self, *args):
            w, h = sc.get_size()
            if (self.myMap.w != w) | (self.myMap.h != h):
                self.myMap.resize(w, h)
                
                self.neptune.setPos(w/2, h/2)

    class Story9:
        def reset(self):
            try:
                self.myMap.clear()
            except:
                pass

        def start(self):
            setLvl(10)
            w, h = sc.get_size()
            self.gameH = 600
            self.nextDialogTime = [time(), 0]
            game.setMap('босс конец')
            self.myMap = game.getMap('босс конец')
            self.reset()
            self.myMap.resize(w, h)
            
            self.hero = Image('images/hero3.png', 400, 400, 50, 100)
            self.neptune = Image(['images/neptune-fight.png', 'images/old-man3.png', 'images/old-man2.png'], 560, 400, 130, 130)
            self.merlins = []
            for i in range(2):
                for j in range(2):
                    self.merlins.append(Image("images/marlin.png", w + 140*i, 160 + 100*j, 150, 75))
            self.money = Image('images/moneys.png', w + 10,  170, 200, 200)
            self.book = Image('images/book0.png', w + 10,  190, 30, 30)

            self.dialogs = [
                [(4, None), 'Ты сражался отлично', .05, 2, 'neptune-cut.png'],
                [(6, lambda: self.myMap.eventHandler.onLoopUpdate.addElement(self.getTreasures)), 'Вот держи сокровиша', .05, .3, 'neptune-cut.png'],
                [(3, lambda: self.neptune.changeImage(1)), '....', .4, .3, 'old-man-cut-hidden.png'],
                [(2, None), '', .05, .3, 'old-man-cut2.png'],
                [(6, lambda: self.neptune.changeImage(2)), 'Что, почему эта рыба стало дедушкой, как так, почему?', .03, .3, 'hero-cut3.png'],
                [(4, None), 'Мм, что это за книга?', .03, .3, 'hero-cut3.png'],
                [(4, None), 'Что же в ней написано', .03, .3, 'hero-cut0.png'],
                [(29, lambda: self.myMap.eventHandler.onLoopUpdate.addElement(self.resizeDialog)), 'Я сегодня плавал. И вдруг начал думать, что живу скучно. Мне захотелось как то разнообразить свою жизнь. И я решил украсть мальчика с деревни. Я стер ему воспоминая, добавил немного о себе и положил спать на полу в доме. Когда он очнулся, я подумал, что будет интересно, если он попытается попасть в мой дворец. И вот я дал ему акваланг и попросил, что бы он помог достать мой сундук. А в сундук я положил свою книгу. Несколько раз он нарушал мои правила. И приходилось заного стерать воспоминания. Но вот он, наконец, попал в мой дворец. и я подумал. Теперь то я повеселюсь. Только сначала надо подготовить подарок', .03, .3, 'hero-cut0.png'],
                ]

            self.actions = [self.nextDialog, self.nextDialog, self.nextDialog, self.nextDialog, self.nextDialog, self.nextDialog, self.nextDialog, self.nextDialog, lambda:game.setMap("главное меню")]
            self.myMap.addElement([self.neptune, self.hero, *self.merlins, self.money, self.book])
            self.myMap.eventHandler.onClick.addElement(self.myMap, self.resetDialogTime)
            self.myMap.eventHandler.onLoopUpdate.addElement(self.actionsPlay)
            self.myMap.eventHandler.onLoopUpdate.addElement(self.onResize)

        def resizeDialog(self):
            dialogManager.bg.resize(h=600)

        def getTreasures(self):
            for i in self.merlins:
                i.moove(-3)
            self.money.moove(-3)
            self.book.moove(-3)
            if self.money.x <= sc.get_size()[0]/2 - 80:
                self.money.moove(3)
                self.book.moove(3)
                for i in self.merlins:
                    i.moove(-5)
                if self.merlins[0].x < -500:
                    self.myMap.eventHandler.onLoopUpdate.delElement(self.getTreasures)

        def setFirstSpawnTime(self):
            self.marlineSpawnTime = time() + 1
            self.marlineSpawnTime2 = time() + 6
            self.mirrirSpawn = time() + 1

        def moove(self):
            w, h = sc.get_size()
            if dialogManager.work: dialogManager.stop()
            self.spawnTornado()
            keys.updateKeys(); speed = 4
            x, y = [(-keys.a + keys.d) * speed, (-keys.w + keys.s) * speed]
            self.hero.moove(x)
            self.hero.moove(y=y)

            
        def resetDialogTime(self, *args):
            self.nextDialogTime[1] = .001
        
        def nextDialog(self, *args):
            if len(self.dialogs) > 0:
                if self.nextDialogTime[1] <= 0:
                    self.nextDialogTime = [time(), self.dialogs[0][0][0]]
                    dialogManager.start(self.myMap, *self.dialogs[0][1:])
                    if self.dialogs[0][0][1]:
                        self.dialogs[0][0][1]()
                else:
                    self.nextDialogTime[1] -= time() - self.nextDialogTime[0]
                    self.nextDialogTime[0] = time()
            if self.nextDialogTime[1] <= 0:
                if len(self.dialogs) > 0:
                    self.dialogs.pop(0)
                    self.actions.pop(0)

        def stopDialog(self):
            dialogManager.stop()
            self.actions.pop(0)

        def actionsPlay(self):
            if len(self.actions) > 0:
                self.actions[0]()

        def onResize(self, *args):
            w, h = sc.get_size()
            if (self.myMap.w != w) | (self.myMap.h != h):
                self.myMap.resize(w, h)
                self.hero.setPos(w/2 - 60, h/2)                
                self.neptune.setPos(w/2, h/2)


# cтавит по центру кнопку играть
def setToCenterWelkomMenu():
    w, h = sc.get_size()
    if w != welkomMenu.w or h != welkomMenu.h:
        setElementToCenterX(playBtn)
        welkomMenu.resize(w,h)

# анимация затемнения экрана
class DarkScreenAnimation:
    actionWithDarkImage = ''
    darkImages = []
    blackImage = Image("images/blackColor.png", 0, 0, 20, 20)
    story = None
    def __init__(self):
        topMap.addElement(self.blackImage)
        self.blackImage.setAlpha(0)
    def newStory(self, story):
        self.story = story
        story.reset()
        self.blackImage.setAlpha(0)
        self.actionWithDarkImage = 'add'
        self.blackImage.setAlpha(0)
        topMap.addElement(self.blackImage)
        topMap.eventHandler.onLoopUpdate.addElement(self.onLoopUpdate)
    
    def onLoopUpdate(self):
        if self.actionWithDarkImage == 'add':
            if self.blackImage.alpha < 255:
                    alpha = self.blackImage.alpha
                    alpha += 10
                    if alpha > 255: alpha = 255
                    self.blackImage.setAlpha(alpha)
            else:
                self.actionWithDarkImage = 'del'
                self.story.start()
        elif self.actionWithDarkImage == 'del':
            if self.blackImage.alpha > 0:
                alpha = self.blackImage.alpha; alpha -= 4
                if alpha < 0: alpha = 0
                self.blackImage.setAlpha(alpha)
            else:
                self.actionWithDarkImage = ''
                topMap.delElement(self.blackImage)
                topMap.eventHandler.onLoopUpdate.delElement(self.onLoopUpdate)
        self.blackImage.resize(*sc.get_size())

# детектор основных клавиш
class Keys:
    w = a = s = d = False
    def updateKeys(self):
        pgKeys = pg.key.get_pressed()
        self.w = pgKeys[pg.K_w]
        self.a = pgKeys[pg.K_a]
        self.s = pgKeys[pg.K_s]
        self.d = pgKeys[pg.K_d]

# ставит уровень открытых локаций, сохраняет текушую доступнуя локацию
def setLvl(lvl):
    global passedLevels
    if passedLevels < lvl:
        passedLevels = lvl
    with open('lvls.txt', 'w') as f:
        f.write(str(passedLevels))
    for i in range(len(storyBtnsEnter)):
        welkomMenu.eventHandler.onClick.delElement(storyBtnsEnter[i])
        welkomMenu.eventHandler.mouseHover.delElement(storyBtnsEnter[i])
        storyBtnsEnter[i].bgColor = [10, 10, 10]
        storyBtnsEnter[i].drawableBgColor = [10, 10, 10]
        if passedLevels >= i + 1:
            storyBtnsEnter[i].bgColor = [120, 120, 120]
            storyBtnsEnter[i].drawableBgColor = [120, 120, 120]
            addButtonHoverEffect(welkomMenu, storyBtnsEnter[i]); storyBtnsEnter[i].id = i+1
            welkomMenu.eventHandler.onClick.addElement(storyBtnsEnter[i], setStory)

# запускает локацию по нажатию кнопок в главном меню
def setStory(el, *args):
    darkScreenAnimation.newStory(storys[el.id-1]())

# регулеровщик кнопки громкости музыки
def mooveSoundBtn(*args):
    pressed = pg.mouse.get_pressed()[0]
    if pressed:
        if isMouseRectCollide(soundRectBtn):
            soundRectBtn.pressed = True
    else:
        soundRectBtn.pressed = False
    if soundRectBtn.pressed:
        x, y = getMousePos()
        soundRectBtn.setPos(x - 10)
        if soundRectBtn.x < soundRectBg.x + 4:
            soundRectBtn.setPos(soundRectBg.x + 4)
        elif soundRectBtn.x > soundRectBg.x + soundRectBg.w - 24:
            soundRectBtn.setPos(soundRectBg.x + soundRectBg.w - 24)
        global sound_volume
        sound_volume = (soundRectBtn.x - soundRectBg.x - 4)/(soundRectBg.w - 28)
        soundLabel.updateText(str(sound_volume))
        pg.mixer.music.set_volume(sound_volume)

def mooveEffectBtn(*args):
    pressed = pg.mouse.get_pressed()[0]
    if pressed:
        if isMouseRectCollide(effectRectBtn):
            effectRectBtn.pressed = True
    else:
        effectRectBtn.pressed = False
    if effectRectBtn.pressed:
        x, y = getMousePos()
        effectRectBtn.setPos(x - 10)
        if effectRectBtn.x < effectRectBg.x + 4:
            effectRectBtn.setPos(effectRectBg.x + 4)
        elif effectRectBtn.x > effectRectBg.x + effectRectBg.w - 24:
            effectRectBtn.setPos(effectRectBg.x + effectRectBg.w - 24)
        global effects_volume
        effects_volume = (effectRectBtn.x - effectRectBg.x - 4)/(effectRectBg.w - 28)
        effectLabel.updateText(str(effects_volume))


# запускает звук
def playSound(sound):
    pg.mixer.Channel(1).play(pg.mixer.Sound(f'sounds\{sound}.wav'))
    pg.mixer.Channel(1).set_volume(effects_volume)

# устанавливет сложность
def setEasy(*args):
    for i in difficultBtns:
        i.bgColor = (200, 200, 200)
        i.drawableBgColor = (200, 200, 200)
    difficultBtn0.bgColor = (150, 150, 150)
    difficultBtn0.drawableBgColor = (100, 100, 100)
    difficultSetting.selfSpeedInArrowMap = 5
    difficultSetting.tornadoSpawnSpeed = 3
    difficultSetting.marlinSpeedSpawnBos = 4
    difficultSetting.marlinWaitSpawnBos = 20
    difficultSetting.mirrorFishWaitSpawn = 6
    difficultSetting.mirrorFishRespawnBos = 1.5 
    difficultSetting.actionAfterDie = 'respawn'

# устанавливет сложность
def setNormal(*args):
    for i in difficultBtns:
        i.bgColor = (200, 200, 200)
        i.drawableBgColor = (200, 200, 200)
    difficultBtn1.bgColor = (150, 150, 150)
    difficultBtn1.drawableBgColor = (100, 100, 100)
    difficultSetting.selfSpeedInArrowMap = 4
    difficultSetting.tornadoSpawnSpeed = 1.8
    difficultSetting.marlinSpeedSpawnBos = 2.5
    difficultSetting.marlinWaitSpawnBos = 7
    difficultSetting.mirrorFishWaitSpawn = 15
    difficultSetting.mirrorFishRespawnBos = 3
    difficultSetting.actionAfterDie = 'respawn'

# устанавливет сложность
def setHard(*args):
    for i in difficultBtns:
        i.bgColor = (200, 200, 200)
        i.drawableBgColor = (200, 200, 200)
    difficultBtn2.bgColor = (150, 150, 150)
    difficultBtn2.drawableBgColor = (100, 100, 100)
    difficultSetting.selfSpeedInArrowMap = 3
    difficultSetting.tornadoSpawnSpeed = .8
    difficultSetting.marlinSpeedSpawnBos = 1.6
    difficultSetting.marlinWaitSpawnBos = 6
    difficultSetting.mirrorFishWaitSpawn = 24
    difficultSetting.mirrorFishRespawnBos = 5 
    difficultSetting.actionAfterDie = 'die :D'

# устанавливет сложность
def setHardcore(*args):
    for i in difficultBtns:
        i.bgColor = (200, 200, 200)
        i.drawableBgColor = (200, 200, 200)
    difficultBtn3.bgColor = (150, 150, 150)
    difficultBtn3.drawableBgColor = (100, 100, 100)

    difficultSetting.selfSpeedInArrowMap = 2
    difficultSetting.tornadoSpawnSpeed = .5
    difficultSetting.marlinSpeedSpawnBos = 1
    difficultSetting.marlinWaitSpawnBos = 3
    difficultSetting.mirrorFishWaitSpawn = 30
    difficultSetting.mirrorFishRespawnBos = 6 
    difficultSetting.actionAfterDie = 'die :D'

# данные используемые для настройки сложности
class DifficultSetting:
    selfSpeedInArrowMap = 3
    tornadoSpawnSpeed = .4
    marlinSpeedSpawnBos = 1
    marlinWaitSpawnBos = 10
    mirrorFishWaitSpawn = 10
    mirrorFishRespawnBos = 2 
    actionAfterDie = 'respawn'

topMap = Map(0, 0, 4000, 4000)
difficultSetting = DifficultSetting()
keys = Keys()
darkScreenAnimation = DarkScreenAnimation()
dialogManager = DialogManager()
gameStory = GameStory()
storys = [gameStory.Story0, gameStory.Story1, gameStory.Story2, gameStory.Story3, gameStory.Story4, gameStory.Story5, gameStory.Story6, gameStory.Story7, gameStory.Story8, gameStory.Story9] 

# инициализация карт, елементов карт
game = Game()
welkomMenu = Map(0, 0, 4000, 4000, (60, 170, 120))
settingsMenu = Map(0, 0, 3000, 3000, (60, 170, 120))

homeFirstSize = (640, 360)
streetFirstSize = (544, 326)
home = Map(0, 0, 640, 360, bgImage="images/house-room.png")
home2 = Map(0, 0, 640, 360, bgImage="images/house-room.png")

tombEnterMap = Map(0, 0, 4000, 2000, bgImage="images/stone-wall.png")
tombArrowsMap = Map(0, 0, 4000, 2000, (60, 120, 216))
labirinthMap = Map(0, 0, 4000, 2000, (60, 120, 216))
bossMap = Map(0, 0, 1000, 1000, bgImage="images/stone-wall2.png")
bossMapEnd = Map(0, 0, 1000, 1000, bgImage="images/stone-wall2.png")
streetMap = Map(0, 0, 544, 326, bgImage="images/street0.png")
waterMap0 = Map(0, 0, 6000, 1200, (207, 226, 243))
waterMap1 = Map(0, 0, 6000, 1200, (207, 226, 243))
waterRect = selfRect(-1000, 200, 8000, 1000, (60, 120, 216))
waterRect1 = selfRect(-1000, 200, 8000, 1000, (60, 120, 216))

backBtn = Button('Назад', 0, 0, fontSize=21)
addButtonHoverEffect(settingsMenu, backBtn)
settingsMenu.eventHandler.onClick.addElement(backBtn, lambda e: game.setMap('главное меню'))

difficultBtn0 = Button('Легко', 50, 400, fontSize=18, size=(80, 30))
difficultBtn1 = Button('Средне', 150, 400, fontSize=18, size=(80, 30))
difficultBtn2 = Button('Тяжело', 250, 400, fontSize=18, size=(80, 30))
difficultBtn3 = Button('Хардкор', 350, 400, fontSize=18, size=(80, 30))
difficultBtns = [difficultBtn0, difficultBtn1, difficultBtn2, difficultBtn3]
addButtonHoverEffect(settingsMenu, difficultBtn0)
addButtonHoverEffect(settingsMenu, difficultBtn1)
addButtonHoverEffect(settingsMenu, difficultBtn2)
addButtonHoverEffect(settingsMenu, difficultBtn3)
settingsMenu.eventHandler.onClick.addElement(difficultBtn0, setEasy)
settingsMenu.eventHandler.onClick.addElement(difficultBtn1, setNormal)
settingsMenu.eventHandler.onClick.addElement(difficultBtn2, setHard)
settingsMenu.eventHandler.onClick.addElement(difficultBtn3, setHardcore)


openSettingBtn = Button('Настройки', 0, 0, fontSize=21)
addButtonHoverEffect(welkomMenu, openSettingBtn)
welkomMenu.eventHandler.onClick.addElement(openSettingBtn, lambda e: game.setMap('настройки'))

soundLabel0 = Label('Громкость музыки', 18, 50, 140)
soundLabel = Label('0.03', 18, 50, 170)
soundRectBg = selfRect(50, 200, 228, 28, (180, 180, 180))
soundRectBtn = Button("", 54, 204, (120, 120, 120), size=[20, 20])
soundRectBtn.pressed = False
addButtonHoverEffect(settingsMenu, soundRectBtn)
settingsMenu.eventHandler.onLoopUpdate.addElement(mooveSoundBtn)
sound_elements = [soundRectBg, soundRectBtn, soundLabel0, soundLabel] 

effectLabel0 = Label('Громкость эффектов', 18, 350, 140)
effectLabel = Label('0.03', 18, 350, 170)
effectRectBg = selfRect(350, 200, 228, 28, (180, 180, 180))
effectRectBtn = Button("", 354, 204, (120, 120, 120), size=[20, 20])
effectRectBtn.pressed = False
addButtonHoverEffect(settingsMenu, effectRectBtn)
settingsMenu.eventHandler.onLoopUpdate.addElement(mooveEffectBtn)
effect_elements = [effectRectBg, effectRectBtn, effectLabel0, effectLabel] 


storyBtns = []
storyBtnsEnter = []
for i in range(10):
    storyBtns.append(Button(f'Квест {i+1}', 18 + 150*(i%5), 298 + 80*(i//5), fontSize=20, size=[104, 64]))
    storyBtnsEnter.append(Button(f'Войти', 20 + 150*(i%5), 330 + 80*(i//5), (130, 130, 130), fontSize=20, size=[100, 30]))

playBtn = Button("Играть", 0, 200)

welkomMenu.addElement([openSettingBtn, playBtn, *storyBtns, *storyBtnsEnter])
settingsMenu.addElement([backBtn, *sound_elements, *effect_elements,*difficultBtns])
addButtonHoverEffect(welkomMenu, playBtn)
setToCenterWelkomMenu()

welkomMenu.eventHandler.onClick.addElement(playBtn, lambda e: darkScreenAnimation.newStory(gameStory.Story0()))
welkomMenu.eventHandler.onLoopUpdate.addElement(setToCenterWelkomMenu)

# добавление карт в менеджера игры
game.addElement(welkomMenu, 'главное меню')
game.addElement(home, 'дом')
game.addElement(home2, 'дом 2')
game.addElement(waterMap0, 'вода 0')
game.addElement(waterMap1, 'вода 1')
game.addElement(streetMap, 'улица')
game.addElement(tombEnterMap, 'храм вход')
game.addElement(tombArrowsMap, 'дорога со стрелами')
game.addElement(labirinthMap, 'лабиринт')
game.addElement(bossMap, 'босс')
game.addElement(bossMapEnd, 'босс конец')
game.addElement(settingsMenu, 'настройки')
game.addElement(topMap, None, True)

sound_volume = 0.03
effects_volume = 0.03

music_list = ['musics/music1.mp3', 'musics/music2.mp3']

with open('lvls.txt', 'r') as f:
    passedLevels = int(f.readlines()[0])

setLvl(passedLevels)
setHard()
oldScreenSize = sc.get_size()
while running:
    if pg.key.get_pressed()[pg.K_ESCAPE]:
        game.setMap('главное меню')
    if not pg.mixer.music.get_busy():
        music_list = music_list[::-1]
        pg.mixer.music.load(music_list[0])
        pg.mixer.music.set_volume(sound_volume)
        pg.mixer.music.play()

    events = pg.event.get()
    game.updateEventHandlerData(events)
    for e in events:
        if e.type == pg.QUIT:
            running = False

    sc.fill(bgColor)
    game.draw()
    pg.display.flip()
    clock.tick(fps)

pg.quit()