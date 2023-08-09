from init import *

def buttonHoverEffect(btn):
    newBgColor = list(btn.bgColor)
    newBgColor[0] -= 50; newBgColor[1] -= 50; newBgColor[2] -= 50
    if newBgColor[0] < 0: newBgColor[0] = 0
    if newBgColor[1] < 0: newBgColor[1] = 0
    if newBgColor[2] < 0: newBgColor[2] = 0
    btn.drawableBgColor = newBgColor

def buttonUnhoverEffect(btn):
    btn.drawableBgColor = btn.bgColor

def addButtonHoverEffect(workMap, element):
    workMap.eventHandler.mouseHover.addElement(element, buttonHoverEffect, buttonUnhoverEffect)

def getMousePos():
    return pg.mouse.get_pos()

def isMouseRectCollide(rect, gameMap=None):
    x, y = getMousePos()
    if gameMap:
        try:
            if not rect.anchor:
                x -= gameMap.x
                y -= gameMap.y
        except:
            x -= gameMap.x
            y -= gameMap.y
            # print("нет атрибута anchor")
    if (rect.x + rect.w >= x >= rect.x):
        if (rect.y + rect.h >= y >= rect.y):
            return True
    
    return False

# обработчик событий
class EventHandler:
    def __init__(self, gameMap=None):
        self.mouseHover = self.MouseHover(gameMap)
        self.onClick = self.OnClick(gameMap)
        self.onKeyPress = self.OnKeyPress()
        self.onLoopUpdate = self.OnLoopUpdate()
    # наведение мыши
    class MouseHover:
        def __init__(self, gameMap=None):
            self.objects = []
            self.objectsOnHover = []
            self.objectsOnUnhover = []
            self.objectsIsHovered = []
            self.gameMap = gameMap

        def clear(self):
            self.objects = []
            self.objectsOnHover = []
            self.objectsOnUnhover = []
            self.objectsIsHovered = []

        def addElement(self, element, onHover=None, onUnhover=None):
            self.objects.append(element)
            self.objectsOnHover.append(onHover)
            self.objectsOnUnhover.append(onUnhover)
            self.objectsIsHovered.append(0)

        def delElement(self, index):
            try:
                if type(index) != int:
                    index = self.objects.index(index)
                    # self.onLoopUpdate.pop(index)
                    self.objects.pop(index)
                    self.objectsOnHover.pop(index)
                    self.objectsOnUnhover.pop(index)
                    self.objectsIsHovered.pop(index)
            except ValueError:
                pass
        
        def run(self):
            itemsAmount = len(self.objects)
            for i in range(itemsAmount):
                if isMouseRectCollide(self.objects[i], self.gameMap):
                    if self.objectsIsHovered[i] == 0:
                        self.objectsIsHovered[i] = 1
                        if self.objectsOnHover[i]: 
                            self.objectsOnHover[i](self.objects[i])
                            break
                else:
                    if self.objectsIsHovered[i] == 1:
                        self.objectsIsHovered[i] = 0
                        if self.objectsOnUnhover[i]: 
                            self.objectsOnUnhover[i](self.objects[i])
                            break
    # по нажатию по елементу мышкой
    class OnClick:
        def __init__(self, gameMap=None):
            self.objects = []
            self.objectsOnClick = []
            self.buttonKeys = []
            self.gameMap = gameMap

        def clear(self):
            self.objects = []
            self.objectsOnClick = []
            self.buttonKeys = []

        def addElement(self, element, onClick=None, button=1):
            self.objects.append(element)
            self.objectsOnClick.append(onClick)
            self.buttonKeys.append(button)
        
        def run(self, button):
            itemsAmount = len(self.objects)
            for i in range(itemsAmount):
                if self.buttonKeys[i] == button:
                    if isMouseRectCollide(self.objects[i], self.gameMap):
                        if self.objectsOnClick[i]: 
                            self.objectsOnClick[i](self.objects[i])
                            break

        def delElement(self, index):
            try:
                if type(index) != int:
                    index = self.objects.index(index)
                self.objects.pop(index)
                self.objectsOnClick.pop(index)
                self.buttonKeys.pop(index)
            except:
                pass
    # по нажатию клавиши
    class OnKeyPress:
        def __init__(self):
            self.onKeyPress = []
            self.buttonKeys = []

        def clear(self):
            self.onKeyPress = []
            self.buttonKeys = []

        def addElement(self, onKeyPress=None, button=[]):
            self.onKeyPress.append(onKeyPress)
            if type(button) == int:
                self.buttonKeys.append([button])
            else:
                self.buttonKeys.append(button)
        
        def delItem(self, index):
            self.onKeyPress.pop(index)
            self.buttonKeys.pop(index)

        def run(self, button, pressed):
            itemsAmount = len(self.onKeyPress)
            for i in range(itemsAmount):
                if button in self.buttonKeys[i]:
                    if self.onKeyPress[i]: self.onKeyPress[i](button, pressed)
    # каждый новый кадр
    class OnLoopUpdate:
        def __init__(self):
            self.onLoopUpdate = []
        
        def addElement(self, onLoopUpdate=None):
            self.onLoopUpdate.append(onLoopUpdate)
        
        def clear(self):
            self.onLoopUpdate = []

        def run(self):
            for i in self.onLoopUpdate:
                if i: i()

        def delElement(self, index):
            if type(index) == int:
                self.onLoopUpdate.pop(index)
            else:
                try:
                    index = self.onLoopUpdate.index(index)
                    self.onLoopUpdate.pop(index)
                except ValueError:
                    pass
    # запускает проверку событий
    def run(self, events):
        self.onLoopUpdate.run()
        for e in events:
            if e.type == pg.MOUSEMOTION:
                self.mouseHover.run()
            elif e.type == pg.MOUSEBUTTONUP:
                self.onClick.run(e.button)
            elif e.type == pg.KEYDOWN: 
                self.onKeyPress.run(e.key, 1)
            elif e.type == pg.KEYUP: 
                self.onKeyPress.run(e.key, 0)

# модель прямоугольника
class selfRect(pg.Rect):
    def __init__(self, x=0, y=0, w=10, h=10, color=None , draw=True, anchor=False):
        super().__init__(x, y, w, h)
        self.drawMe = draw
        self.anchor = anchor
        self.color = color

    def draw(self):
        if self.color:
            pg.draw.rect(sc, self.color, self)

    def setPos(self, x=None, y=None):
        if x != None:
            self.x = x
        if y != None:
            self.y = y

    def moove(self, x=0, y=0):
        self.x += x; self.y += y

# игровая модель
class Game():
    def __init__(self):
        self.objects = []
        self.topObjects = []
        self.objectsName = []
        self.currentMap = -1
        self.events = pg.event.get()

    def updateEventHandlerData(self, events):
        self.events = events

    def addElement(self, element, name=None, top=False):
        if top:
            self.topObjects.append(element)
        else:
            self.objects.append(element)
            self.objectsName.append(name)
            if self.currentMap == -1: self.currentMap = 0

    def setMap(self, index):
        if type(index) == int: 
            self.currentMap = index
            return 1
        if type(index) == str:
            for i in range(len(self.objectsName)):
                if self.objectsName[i] != None:
                    if self.objectsName[i] == index:
                        self.currentMap = i
                        return 1
                    
        print("Данная карта не найдена")
        return 0
    
    def getMap(self, index):
        if type(index) == str:
            for i in range(len(self.objectsName)):
                if self.objectsName[i] != None:
                    if self.objectsName[i] == index:
                        return self.objects[i]
        elif type(index) == int:
            return self.objects[index]
    
    def draw(self):
        if self.currentMap != -1: self.objects[self.currentMap].draw(); self.objects[self.currentMap].eventHandler.run(self.events)
        for i in self.topObjects:
            i.draw()
            i.eventHandler.run(self.events)

# карта, содержит обработчик событий, елементы отрисовки
class Map(pg.Rect):
    def __init__(self, x=0, y=0, w=scSize[0], h=scSize[1], bgColor=None, bgImage=None):
        super().__init__(x, y, w, h)
        
        self.topMap = []
        self.objects = []
        self.bgColor = bgColor
        self.anchoredCameraElement = None

        self.bgImage = bgImage
        if bgImage:
            img = pg.image.load(bgImage)
            img.convert()
            self.bgImage = pg.transform.scale(img, (w, h))
            self.imagePath = bgImage

        self.eventHandler = EventHandler(self)

    def addElement(self, element):
        if type(element) == list or type(element) == list:
            for i in element:
                self.objects.append(i)
        else:
            self.objects.append(element)

    def clear(self):
        self.x = 0; self.y = 0
        self.eventHandler.mouseHover.clear()
        self.eventHandler.onClick.clear()
        self.eventHandler.onKeyPress.clear()
        self.eventHandler.onLoopUpdate.clear()
        self.anchoredCameraElement = None
        self.objects = []

    def delElement(self, element):
        try: 
            index = self.eventHandler.mouseHover.objects.index(element)
            self.eventHandler.mouseHover.delElement(index)
        except: pass
        try: 
            index = self.eventHandler.onClick.objects.index(element)
            self.eventHandler.onClick.delElement(index)
        except: pass
        try:
            index = self.objects.index(element)
            self.objects.pop(index)
        except: pass

    def resize(self, w=None, h=None):
        if w: self.w = w
        if h: self.h = h
        self.updateBgImageSize()

    def updateBgImageSize(self):
        if self.bgImage:
            img = pg.image.load(self.imagePath)
            img.convert()
            self.bgImage = pg.transform.scale(img, (self.w, self.h))


    def anchorCameraAtElement(self, element=None, x=0, y=0):
        self.anchoredCameraElement = element

    def draw(self):
        if self.anchoredCameraElement:
            mooveDistance = (self.anchoredCameraElement.x - (sc.get_width()/2 - self.anchoredCameraElement.w/2),
                self.anchoredCameraElement.y - (sc.get_height()/2 - self.anchoredCameraElement.h/2)
            )
            self.x = -mooveDistance[0]; self.y = -mooveDistance[1]

        if self.bgImage:
            sc.blit(self.bgImage, self)
        elif self.bgColor:
            pg.draw.rect(sc, self.bgColor, self)
        for i in self.objects:
            if not i.anchor:
                i.moove(self.x, self.y)
                i.draw()
                i.moove(-self.x, -self.y)
            elif i != self.anchoredCameraElement:
                i.draw()
            else:
                savedPos = (i.x, i.y)
                i.setPos(sc.get_width()/2 - i.w/2, sc.get_height()/2 - i.h/2)
                i.draw()
                i.setPos(*savedPos)
        for i in self.topMap:
            i.draw()

# текстовая модель
class Label(pg.Rect):
    def __init__(self, text="Пусто", size=mainFontSize, x=0, y=0, color=(0, 0, 0), style=mainFontStyle, anchor=False, draw=True):
        self.anchor = anchor; self.drawMe = draw
        self.font = pg.font.SysFont(style, size, False, True)

        self.text = text
        self.color = color
        self.model = self.font.render(self.text, True, self.color)

        self.size = list(self.model.get_size())

        super().__init__(x, y, *self.size)

    def draw(self):
        if self.drawMe: sc.blit(self.model, (self.x, self.y))
        self.size = list(self.model.get_size())
        self.w = self.size[0]
        self.h = self.size[1]

    def updateText(self, text):
        self.model = self.font.render(text, True, self.color)
        self.size = list(self.model.get_size())

    def setPos(self, x=None, y=None):
        if x != None:
            self.x = x
        if y != None:
            self.y = y

    def moove(self, x=0, y=0):
        self.x += x; self.y += y

# кнопка
class Button(pg.Rect):
    def __init__(self, text="Пусто", x=0, y=0, bgColor=(200, 200, 200), fontSize=mainFontSize, fontColor=(0, 0, 0), fontStyle=mainFontStyle, padding=(5 ,5, 5, 5), size=None, anchor=False, draw=True):
        self.anchor = anchor; self.drawMe = draw
        self.bgColor = bgColor; self.drawableBgColor = bgColor
        self.padding = padding
        self.font = pg.font.SysFont(fontStyle, fontSize, False, True)

        self.text = text
        self.textPos = (x + self.padding[3], y + self.padding[0])
        self.fontColor = fontColor
        self.model = self.font.render(self.text, True, self.fontColor)

        if (size == None):
            newSize = list(self.model.get_size())
            newSize[0] += padding[1] + padding[3]
            newSize[1] += padding[0] + padding[2]
        else:
            newSize = size

        super().__init__(x, y, *newSize)

    def updateText(self, text):
        self.model = self.font.render(text, True, self.fontColor)

    def draw(self):
        if self.drawMe:
            pg.draw.rect(sc, self.drawableBgColor, self)
            sc.blit(self.model, self.textPos)

    def setPos(self, x=None, y=None):
        if x != None:
            self.x = x
        if y != None:
            self.y = y
        self.textPos = (self.x + self.padding[3], self.y + self.padding[0])

    def moove(self, x=0, y=0):
        self.x += x; self.y += y
        self.textPos = (self.x + self.padding[3], self.y + self.padding[0])

# картинки
class Image(pg.Rect):
    def __init__(self, path=None, x=0, y=0, w=20, h=20, anchor=False, draw=True, bgColor=None):
        self.anchor = anchor; self.images = []; self.drawMe = draw; self.alpha = 255
        self.imagesPath = [] 
        self.imgIndex = 0
        if type(path) == str:
            self.imagesPath.append(path)
            img = pg.image.load(path)
            img.convert_alpha()
            self.images.append(pg.transform.scale(img, (w, h)))
        else:
            for i in path:
                self.imagesPath.append(i)
                img = pg.image.load(i)
                self.images.append(pg.transform.scale(img, (w, h)))

        self.model = self.images[0]
        self.updatAlpha()
        self.bgColor = bgColor
        super().__init__(x, y, w, h)

    def flip(self):
        for i in self.images:
            cl = i
            i = pg.transform.flip(cl, True, False)
            self.images[self.images.index(cl)] = i
        self.model = self.images[self.imgIndex]

    def draw(self):
        if self.drawMe: 
            if self.bgColor:
                pg.draw.rect(sc, self.bgColor, self)
            sc.blit(self.model, self)

    def setAlpha(self, alpha):
        self.alpha = alpha
        self.updatAlpha()
        

    def updatAlpha(self):
        for i in self.images:
            i.set_alpha(self.alpha)
        self.model = self.images[self.imgIndex]

    def changeImage(self, index):
        self.model = self.images[index]
        self.imgIndex = index

    def resize(self, w=None, h=None):
        if w: self.w = w
        if h: self.h = h
        for i in range(len(self.imagesPath)):
            img = pg.image.load(self.imagesPath[i])
            img.convert_alpha()
            self.images[i] = pg.transform.scale(img, (self.w, self.h))
        self.model = self.images[0]
        self.updatAlpha()

    def setPos(self, x=None, y=None):
        if x != None:
            self.x = x
        if y != None:
            self.y = y

    def moove(self, x=0, y=0):
        self.x += x; self.y += y