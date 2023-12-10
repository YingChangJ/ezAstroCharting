import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib import font_manager
import math


zodiac_symbols = ["♈︎", "♉︎", "♊︎", "♋︎", "♌︎", "♍︎", "♎︎", "♏︎", "♐︎", "♑︎", "♒︎", "♓︎"]
planets_symbols = ["☉","☽","☿","♀",'♂','♃','♄','♅','♆','♇','☊','☋','⚸',"\u2BDE",'🜨︎','⚷',"\u2BDB","⚳","⚴","⚵","⚶"]

class Charting():
    def __init__(self, usingFont = True, fontRelativePath = 'Astronomicon.ttf',colortheme = ['r', '#D69A0A', 'b', 'g'],style_index = 0):
        self.font(usingFont, fontRelativePath)
        self.colortheme = colortheme
        self.style_change(style_index)
        self.fig, self.ax = plt.subplots()
        self.fig.set_facecolor('#e7e7e7')
        circle_out = plt.Circle((0, 0), self.radius_out, edgecolor='k', facecolor='w', fill=True, linewidth=self.linewidth_wide)
        plt.gca().add_patch(circle_out)
        circle_zodiac = plt.Circle((0, 0), self.radius_zodiac, edgecolor='k', fill=False)
        plt.gca().add_patch(circle_zodiac)
        circle_house = plt.Circle((0, 0), self.radius_house, edgecolor='k', fill=False)
        plt.gca().add_patch(circle_house)
        circle_inner = plt.Circle((0, 0), self.radius_inner, edgecolor='k', fill=False)
        plt.gca().add_patch(circle_inner)
        # 设置坐标轴的等比例
        plt.axis('equal')
        # 关闭坐标轴显示
        plt.axis('off')
        # 关闭图例显示
        plt.legend().set_visible(False)
        
    def style_change(self,style_index):    
        self.style_index = style_index
        self.radius_out = 4
        if style_index == 0:
            self.radius_zodiac = 3.2
        else:
            self.radius_zodiac = 3.5 
        self.radius_house = 1.8
        self.radius_inner = 1.5

        self.radius_planet = self.radius_zodiac * 0.8 + self.radius_house * 0.2
        self.radius_planet_degree = self.radius_zodiac * 0.57 + self.radius_house * 0.43
        self.radius_planet_zodiac = self.radius_zodiac * 0.36 + self.radius_house * 0.64
        self.radius_planet_minute = self.radius_zodiac * 0.205 + self.radius_house * 0.795
        self.radius_planet_retro = 1.905


        self.fontsize_planet = 12
        self.fontsize_degree = 7
        self.fontsize_zodiac = 8
        self.fontsize_minute = 5
        self.fontsize_retro = 5

        self.short_length_pl = 0.1
        self.short_length_xtick_minor = 0.15
        self.short_length_xtick_major = 0.3

        self.linewidth_wide = 2
        self.linewidth_middle = 1
        self.linewidth_thin = 1
        self.linewidth_light = 0.3

        self.diff = 6     
    def font(self,usingFont = False, fontRelativePath = ''):
        self.usingFont = usingFont
        if usingFont:
            # Specify the path to the font file
            font_path = fontRelativePath  # Replace with the actual path to your font file
            # Create a FontProperties object with the specified font file
            self.custom_font = font_manager.FontProperties(fname=font_path)
            self.planets_symbols = ['Q','R','S','T','U','V','W','X','Y','Z','g','i','z','⚸','>','q','r','l','m','n','o']
            self.zodiac_symbols = ['A','B','C','D','E','F','G','H','I','J','K','L']
        else:
            self.planets_symbols = planets_symbols
            self.zodiac_symbols = zodiac_symbols

    def _middle(self,deg1,deg2):
        """ 
        Find the middle degree.
        deg1 and deg2 in degree, deg1 >= deg2
        """
        middle = (deg1 + deg2)/2
        if deg1 < deg2:
            middle = (middle + 180)%360
        return middle        
    def _even(self,degrees):
        """ make the planets look evenly, not crowded """
        n = len(degrees)
        groups = [[[i], degrees[i], 0] for i in range(n)] # group element, center, radius
        for _ in range(10): # could be while True:
            flag = True
            index = 0
            while(index<len(groups)):
                groups_n = len(groups)
                next_index = (index+1) % groups_n
                if groups[index][1]<groups[next_index][1]:
                    if groups[index][1]+groups[index][2]+self.diff>groups[next_index][1] - groups[next_index][2]:
                        groups[index][0] += groups[next_index][0]
                        groups[index][1] = self._middle(degrees[groups[index][0][-1]],degrees[groups[index][0][0]])
                        groups[index][2] = (len(groups[index][0])-1) * self.diff / 2
                        groups.pop(next_index)
                        flag = False
                    else:
                        index += 1
                else:
                    if groups[index][1]+groups[index][2]+self.diff>groups[next_index][1]+360 - groups[next_index][2]:
                        groups[index][0] += groups[next_index][0]
                        groups[index][1] = self._middle(degrees[groups[index][0][-1]],degrees[groups[index][0][0]])
                        groups[index][2] = (len(groups[index][0])-1) * self.diff / 2
                        groups.pop(next_index)
                        flag = False
                    else:
                        index += 1
            if flag:
                break
        for group in groups:
            n = len(group[0])
            if n == 1:
                continue
            middle = group[1]
            for index,i in enumerate(group[0]):
                degrees[i] = (middle - group[2] + self.diff * index)%360   
        return degrees

    def _short(self,start_radius,theta,length,width,color = 'k'):
        cos_value = math.cos(math.radians(theta-self.asc))
        sin_value = math.sin(math.radians(theta-self.asc))
        end_radius = start_radius - length
        plt.plot([-start_radius*cos_value, -end_radius*cos_value], [-start_radius*sin_value, -end_radius*sin_value], linewidth=width, color=color, solid_capstyle='butt')
    def _char(self,char,start_radius,theta,color = 'k',fontsize = 12,fontweight='regular',isPlanet = False):
        cos_value = math.cos(math.radians(theta-self.asc))
        sin_value = math.sin(math.radians(theta-self.asc))
        if isPlanet and self.usingFont:
            self.ax.text(-start_radius*cos_value, -start_radius*sin_value, str(char), fontsize=fontsize,fontweight=fontweight, ha='center', va='center',color = color,path_effects=[pe.withStroke(linewidth=self.linewidth_middle, foreground="w")],fontproperties=self.custom_font)
        else:
            self.ax.text(-start_radius*cos_value, -start_radius*sin_value, str(char), fontsize=fontsize,fontweight=fontweight, ha='center', va='center',color = color,path_effects=[pe.withStroke(linewidth=self.linewidth_middle, foreground="w")])
    def _colorIndex(self,degree):
        return int(degree//30%4)
    def _deg2signdeg(self,degree):
        degree_int = int(degree%30)
        sign = int(degree//30)
        minute_int = int(degree*60%60)
        return degree_int, sign, minute_int
    # 绘制直线
    def natal(self,planets = [0,1,2,3,4,5,6,7,8,9,10,11], degrees = [3,5,10,20.0,25,47,90,250,358,359,55,238], houses = [0,30,56.55,70,80,120,180,210,236,250,260,300], asc = 56.55, mc = 300,retro_planet = [10,11],):
        # 绘制圆形
        # self.font(True)
        self.asc = asc
        # 使用 zip 将两个列表配对
        paired_lists = list(zip(planets, degrees))
        # 使用 sorted 对配对的元素进行排序，以 list2 为排序的依据
        sorted_paired_lists = sorted(paired_lists, key=lambda x: x[1])
        # 使用 zip 再次拆分排序后的元素
        planets, degrees = zip(*sorted_paired_lists)
        degrees_even = self._even(list(degrees))

        if asc in houses:
            index_asc = houses.index(asc)
            index_mc = houses.index(mc)
        else:
            largest = max(houses)
            index_asc = houses.index(max((cusp for cusp in houses if cusp <= asc),default=largest))
            index_mc = houses.index(max((cusp for cusp in houses if cusp <= mc),default=largest))

        inner_loop = (self.radius_inner+self.radius_house)/2
        if self.style_index == 0:  
            outer_loop = (self.radius_out*.56 + self.radius_zodiac*.44)   
        else:
            outer_loop = (self.radius_out + self.radius_zodiac)/2  
        for index,house in enumerate(houses):

            width = self.linewidth_light
            self._short(self.radius_inner,house,-self.radius_zodiac+self.radius_inner,width)

            cusp_degree, cusp_sign, cusp_minute = self._deg2signdeg(house)
            if self.style_index == 1:
                self._char(cusp_degree,outer_loop,house - 5,fontsize=self.fontsize_degree,fontweight='semibold')
                self._char(zodiac_symbols[cusp_sign],outer_loop,house,fontsize=self.fontsize_zodiac + 2,color=self.colortheme[cusp_sign%4])
                self._char(cusp_minute,outer_loop,house +5,fontsize=self.fontsize_minute,color='grey')
                
            middle = self._middle(houses[(index+1)%12], house)
            self._char((index-index_asc)%12+1,inner_loop,middle,fontsize=5)
        for house in [asc,mc]:
            width = self.linewidth_wide
            self._short(self.radius_inner,house,-self.radius_zodiac+self.radius_inner,width)         
            self._short(-self.radius_inner,house,self.radius_zodiac-self.radius_inner,width)
            if self.style_index == 0:
                cusp_degree, _, cusp_minute = self._deg2signdeg(house)
                radius_asc_degree = self.radius_zodiac * 0.8 + self.radius_out * 0.2
                print('${}^{}$'.format(cusp_degree, cusp_minute))
                self._char('${}^{{{}}}$'.format(cusp_degree, cusp_minute),radius_asc_degree,house,fontsize=self.fontsize_minute)
        if self.style_index == 0:         
            for degree in range(360):
                length = self.short_length_xtick_minor if degree%10 else self.short_length_xtick_major
                width =  self.linewidth_light if degree%5 else self.linewidth_thin
                if degree%30 == 0:
                    if self.style_index == 0:
                        length = self.radius_out - self.radius_zodiac
                        # 添加文本
                        self._char(zodiac_symbols[degree//30],outer_loop,degree+15,self.colortheme[self._colorIndex(degree)])      
                self._short(self.radius_zodiac,degree,-length,width)
        for planet,degree,degree_even in zip(planets,degrees,degrees_even):
            element = self._colorIndex(degree)
            color = self.colortheme[element]
            self._short(self.radius_zodiac,degree,self.short_length_pl,self.linewidth_middle,color=color)
            planet_sign = self.planets_symbols[planet] if (isinstance(planet, int) and planet < 21) else planet
            self._char(planet_sign,self.radius_planet,degree_even,color=color,fontsize=self.fontsize_planet,isPlanet=True)
            degreeInt, signIndex, minuteInt = self._deg2signdeg(degree)
            self._char(degreeInt,self.radius_planet_degree,degree_even,color='k',fontsize=self.fontsize_degree)
            self._char(zodiac_symbols[signIndex],self.radius_planet_zodiac,degree_even,color=color,fontsize=self.fontsize_zodiac)
            self._char(minuteInt,self.radius_planet_minute,degree_even,color='k',fontsize=self.fontsize_minute)
            if planet in retro_planet:
                self._char('℞',self.radius_planet_retro,degree_even,color=color,fontsize=self.fontsize_retro)
        # self.ax.text(0, 0, '$x^{12}$', ha='center', va='center')

        # 保存为SVG
        plt.savefig('output_vector_graph.svg', format='svg', bbox_inches='tight')
        # 显示图形
        plt.show()

if __name__ == '__main__':
    # Charting(style_index=1).natal()
    Charting(style_index=0).natal()