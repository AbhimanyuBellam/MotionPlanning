import math, sys, pygame, random
from math import *
from pygame import *
import numpy as np
import matplotlib.pyplot as plt
import math
from openpyxl import Workbook
import xlsxwriter


class Node(object):
    def __init__(self,point,parent,cost):
        self.point=point
        self.parent=parent
        self.cost=cost

def dist_btw(p1,p2):
    return sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))

def go_from_pt1_to_pt2(p1,p2):
    if dist_btw(p1,p2) < delta:
        return p2
    else:
        theta = atan2(p2[1]-p1[1],p2[0]-p1[0])
        return p1[0] + delta*cos(theta), p1[1] + delta*sin(theta)

x_size=90
y_size=750
window_size=[x_size,y_size]
delta=10.0
no_of_nodes=5000
pygame.init()
#fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode(window_size)
#colours
white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
green = 0, 255, 0
blue= 0, 0, 255
cyan = 0,180,105
dark_green = 0, 102, 0
brick=156,102,31
darkorange=255,140,0
#rectangles

number_of_cars=6
start_rects=[]
x_ranges=[10,40,70]
for i in range(number_of_cars):
    random_x=x_ranges[random.randint(0,2)]
    random_y=15*random.randint(30,45)
    start_rect=pygame.Rect((random_x,random_y),(10,15))
    start_rects.append(start_rect)
    pygame.draw.rect(screen,green,start_rect)
    pygame.display.update()

goal_rects=[]
for i in range(number_of_cars):
    random_x=x_ranges[random.randint(0,2)]
    random_y=15*random.randint(1,25)
    goal_rect=pygame.Rect((random_x,random_y),(10,15))
    goal_rects.append(goal_rect)
    pygame.draw.rect(screen,red,goal_rect)
    pygame.display.update()

def make_elliptical_field(rect_list):
    ellipse_field_list=[]
    for i in range(len(rect_list)):
        extended_rect_x=rect_list[i][0]-3
        extended_rect_y=rect_list[i][1]-4
        extended_rect=pygame.Rect((extended_rect_x,extended_rect_y),(16,23))
        ellipse_field=pygame.draw.ellipse(screen,black,extended_rect,2)
        ellipse_field_list.append(ellipse_field)
    return ellipse_field_list


times_to_come=[]
time_step=0
for i in range(number_of_cars):
    time_step=time_step+random.randint(1,5)
    times_to_come.append(time_step)

class Car:
    def __init__(car_num,start_node,start_rect,goal_node,goal_rect,time_of_arrival):
        self.car_num=car_num
        self.start_node=start_node
        self.start_rect=start_rect
        self.goal_rect=goal_rect
        self.goal_node=goal_node
        self.time_of_arrival=time_of_arrival



    def collision_with_its_final_rect(p):
        if self.goal_rect.collidepoint(p)== True:
            return True
        return False

def collision_with_obstacle(p):
    if obstacle_ellipse_field.collidepoint(p)== True or obstacle_extended_rect2.collidepoint(p)==True or obstacle_ellipse_field3.collidepoint(p)==True:
        return True
    return False



def get_a_collision_free__random_point(start_point):
    while True:
        p = random.random()*x_size, random.random()*y_size
        p2=(p[0]+100,p[1])
        p3=(p[0]+100,p[1]-70)
        p4=(p[0],p[1]-70)
        if collision_with_obstacle(p)== False and  p[1]<start_point.point[1] and collision_with_obstacle(p2)==False and  collision_with_obstacle(p3)==False and collision_with_obstacle(p4)==False and p[0]<450:
            needed_points1=get_points_in_linesegment(p,p2)
            needed_points2=get_points_in_linesegment(p2,p3)
            needed_points3=get_points_in_linesegment(p3,p4)
            needed_points4=get_points_in_linesegment(p4,p)
            all_needed_points=[needed_points1,needed_points2,needed_points3,needed_points4]
            truth_list=[]
            for i in all_needed_points:
                for j in range(len(i)):
                    if collision_with_obstacle(i[j])==False:
                        truth_list.append(False)
                    else:
                        truth_list.append(True)
                    flag=False
                    for k in range(len(truth_list)):
                        if truth_list[k]==True:
                            flag=True
                            break
                    if flag==False:
                        return p


def get_points_in_linesegment(pt1,pt2):
    points_list=[() for j in range(10)]
    x_part=(pt1[0]+pt2[0])
    y_part=(pt1[1]+pt2[1])
    for i in range(10):
        x_part=x_part/1.12
        y_part=y_part/1.12
        points_list[i]=(x_part,y_part)
    return points_list


def change_parent(curr_node,radius,nodes_list):
    temp_parent=curr_node.parent
    x=int(curr_node.point[0])
    y=int(curr_node.point[1])
    circular_field=pygame.draw.circle(screen,white,(x,y),int(radius),1)
    l=[]
    for i in range(len(nodes_list)):
        p=nodes_list[i]
        if circular_field.collidepoint(p.point):
            #print 'point inside=',p.point
            #print "yaa"
            l.append(p)
    costs=[]
    j=0
    while j<(len(l)):
        costs.append(l[j].cost)
        if costs[-1]==0.0:
            costs.pop()
            l.remove(l[j])
        j=j+1
    #print 'wow'
# print 'distances=',distances
    if len(costs)!=0:
        index_no=costs.index(min(costs))
        #print 'index=',index_no
        #print 'currentnode=',curr_node.point
        
        #print 'actual=',temp_parent.point
        curr_node.parent=l[index_no]
        
        #print 'parentnode=',curr_node.parent.point
        if curr_node==curr_node.parent:
            curr_node.parent=temp_parent
        #print 'hi'

        points_on_line_seg=get_points_in_linesegment(curr_node.point,curr_node.parent.point)
        
        for pt in points_on_line_seg:
            if collision_with_obstacle(pt)==True:
                curr_node.parent=temp_parent

#print curr_node.parent.point

def main():
    
    workbook = xlsxwriter.Workbook('rrt_St_vals.xlsx')
    worksheet = workbook.add_worksheet()
    
    start_point=Node([100-50,600],None,0)
    goal_point=Node([100-50,50],None,0)
    nodes=[]
    nodes.append(start_point)
    present_state='to_get_rrt'
    
    screen.fill(white)
    pygame.draw.rect(screen,green,start_rect)
    pygame.draw.rect(screen,red,goal_rect)
    pygame.draw.rect(screen,black,obstacle_rect)
    pygame.draw.rect(screen,black,obstacle_rect2)
    pygame.draw.rect(screen,black,obstacle_rect3)
    #pygame.draw.rect(screen,black,obstacle_extended_rect,2)
    pygame.draw.line(screen,black,[150,0],[150,900],3)
    pygame.draw.line(screen,black,[300,0],[300,900],3)
    pygame.draw.line(screen,black,[450,0],[450,900],3)
    pygame.draw.ellipse(screen,black,obstacle_extended_rect,2)
    pygame.draw.ellipse(screen,black,obstacle_extended_rect2,2)
    pygame.draw.ellipse(screen,black,obstacle_extended_rect3,2)
    pygame.display.update()
    count=0
    reached=False
    plot_nodes=[]
    x_cords_plt=[]
    y_cords_plt=[]
    cost1=0
    cost2=0
    cost3=0
    cost4=0
    while True:
        
        if present_state=='goal_reached' and reached==False:
            
            pres_node=goal_node
            pygame.display.set_caption('Goal Reached')
            print "Goal Reached"
            print "goal_node=",goal_node
            print 'presentnode=',pres_node.point
            reached=True
            
            print pres_node.parent.point
            print pres_node.parent.parent.point
            print pres_node.parent.parent.parent.point
            
            while pres_node.parent!=None :
                
                
                if pres_node.point[1]>pres_node.parent.point[1]:
                    pres_node.parent=pres_node.parent.parent
                
                pygame.draw.line(screen,red,pres_node.point,pres_node.parent.point,3)
                plot_nodes.append(pres_node)
                needed_point_x=int(plot_nodes[-1].point[0])
                needed_point_y=int(plot_nodes[-1].point[1])
                needed_point=(needed_point_x,needed_point_y)
                main_rect=pygame.Rect((needed_point_x,needed_point_y),(50,70))
                pygame.draw.rect(screen,green,main_rect,2)
                print 'pres_node.parent=',pres_node.parent.point
                pres_node=pres_node.parent
                x_cords_plt.append(plot_nodes[-1].point[0])
                y_cords_plt.append(-1*plot_nodes[-1].point[1])
                print 'point=',plot_nodes[-1].point
            #plt.plot(x_cords_plt,y_cords_plt)
            #plt.show()
            
            
        elif present_state=='to_get_rrt':
            count=count+1
            pygame.display.set_caption('creating RRT')
            if count< no_of_nodes:
                found_next_node=False
                while found_next_node==False:
                    rand=get_a_collision_free__random_point(start_point)
                    rand2=get_a_collision_free__random_point(start_point)
                    rand3=get_a_collision_free__random_point(start_point)
                    rand4=get_a_collision_free__random_point(start_point)
                    
                    #put a condition to check again if the pts fuck up
                    parent_node=nodes[0]
                    for n in nodes:
                        if dist_btw(n.point,rand)<=dist_btw(parent_node.point,rand):
                            new_point=go_from_pt1_to_pt2(n.point,rand)
                            new_point2=go_from_pt1_to_pt2(n.point,rand2)
                            new_point3=go_from_pt1_to_pt2(n.point,rand3)
                            new_point4=go_from_pt1_to_pt2(n.point,rand4)
                            if collision_with_obstacle(new_point)==False and collision_with_obstacle(new_point2)==False and collision_with_obstacle(new_point3)==False and collision_with_obstacle(new_point4)==False:
                                parent_node=n
                                #print 'ya'
                                if new_point[1]<parent_node.point[1] and new_point2[1]<parent_node.point[1] and new_point2[1]<parent_node.point[1] and new_point4[1]<parent_node.point[1]:
                                    found_next_node=True
            
                new_node=go_from_pt1_to_pt2(parent_node.point,rand)
                new_node2=go_from_pt1_to_pt2(parent_node.point,rand2)
                new_node3=go_from_pt1_to_pt2(parent_node.point,rand3)
                new_node4=go_from_pt1_to_pt2(parent_node.point,rand4)
                
                cost1=cost1+dist_btw(parent_node.point,rand)
                cost2=cost2+dist_btw(parent_node.point,rand2)
                cost3=cost3+dist_btw(parent_node.point,rand3)
                cost4=cost4+dist_btw(parent_node.point,rand4)
                
                node1=Node(new_node,parent_node,cost1)
                node2=Node(new_node2,parent_node,cost2)
                node3=Node(new_node3,parent_node,cost3)
                node4=Node(new_node4,parent_node,cost4)
                
                nodes.append(node1)
                nodes.append(node2)
                nodes.append(node3)
                nodes.append(node4)
                #print 'node1=',node1.point
                #print 'node2=',node2.point
                #print 'node3=',node3.point
                #print 'node4=',node4.point
                
                length_of_nodes=len(nodes)
                radius=500.0* math.sqrt((math.log(length_of_nodes)/length_of_nodes))
                
                change_parent(node1,radius,nodes)
                change_parent(node2,radius,nodes)
                change_parent(node3,radius,nodes)
                change_parent(node4,radius,nodes)
                
                #print 'point=',nodes[-1].point
                pygame.draw.line(screen,brick,parent_node.point,new_node)
                pygame.draw.line(screen,blue,parent_node.point,new_node2)
                pygame.draw.line(screen,dark_green,parent_node.point,new_node3)
                pygame.draw.line(screen,darkorange,parent_node.point,new_node4)
                
                if collision_with_final_rect(new_node) :
                    goal_node=node1
                    present_state='goal_reached'
                if collision_with_final_rect(new_node2):
                    goal_node=node2
                    present_state='goal_reached'
                if collision_with_final_rect(new_node3):
                    goal_node=node3
                    present_state='goal_reached'
                if collision_with_final_rect(new_node4):
                    goal_node=node4
                    present_state='goal_reached'
        
            else:
                print "out of nodes"
                return
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                         #pygame.image.save(screen,"rrt_image.png")
                pygame.quit(); sys.exit()
                print 'points=',nodes.point


        pygame.display.update()

#fpsClock.tick(10)


if __name__== '__main__':
    main()


















