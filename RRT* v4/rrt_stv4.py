import math, sys, pygame, random
from math import *
from pygame import *
import bezier
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.artist
import math

x_size=600
y_size=1000
window_size=[x_size,y_size]
delta=50.0
no_of_nodes=5000
pygame.init()
#fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode(window_size)
#colours
white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
blue = 0, 255, 0
green = 0, 0, 255
cyan = 0,180,105
dark_green = 0, 102, 0
brick=156,102,31
darkorange=255,140,0
#rectangles
start_rect=pygame.Rect((100-50,600),(50,70))
goal_rect=pygame.Rect((100-50,50),(50,70))

obstacle_rect=pygame.Rect((100-50,300),(50,70))
obstacle_extended_rect=pygame.Rect((70-50,270),(110,130))
obstacle_ellipse_field=pygame.draw.ellipse(screen,black,obstacle_extended_rect,2)

obstacle_rect2=pygame.Rect((250-50,350),(50,70))
obstacle_extended_rect2=pygame.Rect((220-50,320),(110,130))
obstacle_ellipse_field2=pygame.draw.ellipse(screen,black,obstacle_extended_rect2,2)

obstacle_rect3=pygame.Rect((250-50,50),(50,70))
obstacle_extended_rect3=pygame.Rect((220-50,20),(110,130))
obstacle_ellipse_field3=pygame.draw.ellipse(screen,black,obstacle_extended_rect3,2)

class Node(object):
    def __init__(self,point,parent):
        self.point=point
        self.parent=parent

def dist_btw(p1,p2):
    return sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))
#return sqrt(abs((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2))

def collision_with_final_rect(p):
    if goal_rect.collidepoint(p)== True:
        return True
    return False

def collision_with_obstacle(p):
    if obstacle_ellipse_field.collidepoint(p)== True or obstacle_ellipse_field2.collidepoint(p)==True or obstacle_ellipse_field3.collidepoint(p)==True:
        return True
    return False

def go_from_pt1_to_pt2(p1,p2):
    if dist_btw(p1,p2) < delta:
        return p2
    else:
        theta = atan2(p2[1]-p1[1],p2[0]-p1[0])
        #print 'p1=',p1[0]
        #print p1[0] + delta*cos(theta)
        return p1[0] + delta*cos(theta), p1[1] + delta*sin(theta)

def get_a_collision_free__random_point():
    while True:
        p = random.random()*x_size, random.random()*y_size
        if collision_with_obstacle(p)== False:
            return p
#fpsClock.tick(1)
#bezier curve
def bezier_curve(nodes):
    all_x_cords=[]
    all_y_cords=[]
    for i in range(len(nodes)):
        all_x_cords.append(nodes[i].point[0])
        all_y_cords.append(-1*nodes[i].point[1])
    print 'all_x_cords=',all_x_cords
    nodes1=np.asfortranarray([all_x_cords,all_y_cords])
    curve = bezier.Curve(nodes1, degree=2)

    x_obs1_cords=[20.0,130,130,20]
    y_obs1_cords=[270.0,270,400,400]
    nodes2=np.asfortranarray([x_obs1_cords,y_obs1_cords])
    curve2=bezier.Curve(nodes2, degree=2)

    x_obs2_cords=[170.0,230,230,170]
    y_obs2_cords=[320.0,320,400,400]
    nodes3=np.asfortranarray([x_obs2_cords,y_obs2_cords])
    curve3=bezier.Curve(nodes3,degree=2)

    x_obs3_cords=[170.0,330,330,170]
    y_obs3_cords=[20.0,20,150,150]
    nodes4=np.asfortranarray([x_obs3_cords,y_obs3_cords])
    curve4=bezier.Curve(nodes3,degree=2)
#curve2.plot(1000)
    #curve3.plot(1000)
    curve.plot(1000)
    plt.show()
    intersects1=curve.intersect(curve2)
    intersects2=curve.intersect(curve3)
    print 'intersection1=',intersects1
    print 'intersection2=',intersects2
    if len(intersects1)!=0:
        for i in range(len(nodes)):
            if i >0 and nodes[i].point[1]<270 and nodes[i].point[1]>nodes[i-1]:
                new_start_point=nodes[i]
                print new_start_point.point
    if len(intersects2)!=0:
        for i in range(len(nodes)):
            if i >0 and nodes[i].point[1]<280 and nodes[i].point[1]>nodes[i-1]:
                new_start_point=nodes[i]
                print new_start_point.point

#print type(curve)
#nodes2=list(curve)
#print nodes2
#s_vals=np.linspace(nodes[0][0],nodes.point[-1] [0], 5)
#nd_array=curve.evaluate_multi(s_vals)
#for i in range(len(nd_array))

#plt.show()
#plt.plot(curve)

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
    distances=[]
    j=0
    while j<len(l):
        distances.append(dist_btw(curr_node.point,l[j].point))
        if distances[-1]==0.0:
            distances.pop()
            l.remove(l[j])
        j=j+1
# print 'distances=',distances
    if len(distances)!=0:
        index_no=distances.index(min(distances))
        #print 'index=',index_no
        #print 'currentnode=',curr_node.point
        
        #print 'actual=',temp_parent.point
        curr_node.parent=l[index_no]
        
        #print 'parentnode=',curr_node.parent.point
        if curr_node==curr_node.parent:
            curr_node.parent=temp_parent

#print curr_node.parent.point

def main():
    start_point=Node([100-50,600],None)
    goal_point=Node([100-50,50],None)
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
    while True:
        
        if present_state=='goal_reached' and reached==False:
            
            pres_node=goal_node.parent
            pygame.display.set_caption('Goal Reached')
            print "Goal Reached"
            print "goal_node=",goal_node
            print 'presentnode=',pres_node.point
            reached=True
            
            print pres_node.parent.point
            print pres_node.parent.parent.point
            print pres_node.parent.parent.parent.point
            
            while pres_node.parent!=None :
                
                pygame.draw.line(screen,red,pres_node.point,pres_node.parent.point,3)
                plot_nodes.append(pres_node)
                print 'pres_node.parent=',pres_node.parent.point
                pres_node=pres_node.parent
                x_cords_plt.append(plot_nodes[-1].point[0])
                y_cords_plt.append(-1*plot_nodes[-1].point[1])
                print 'point=',plot_nodes[-1].point
            #plt.plot(x_cords_plt,y_cords_plt)
            #plt.show()
            bezier_curve(plot_nodes)
            
        elif present_state=='to_get_rrt':
            count=count+1
            pygame.display.set_caption('creating RRT')
            if count< no_of_nodes:
                found_next_node=False
                while found_next_node==False:
                    rand=get_a_collision_free__random_point()
                    rand2=get_a_collision_free__random_point()
                    rand3=get_a_collision_free__random_point()
                    rand4=get_a_collision_free__random_point()
                    parent_node=nodes[0]
                    for n in nodes:
                        if dist_btw(n.point,rand)<=dist_btw(parent_node.point,rand):
                            new_point=go_from_pt1_to_pt2(n.point,rand)
                            if collision_with_obstacle(new_point)==False:
                                parent_node=n
                                found_next_node=True
                new_node=go_from_pt1_to_pt2(parent_node.point,rand)
                new_node2=go_from_pt1_to_pt2(parent_node.point,rand2)
                new_node3=go_from_pt1_to_pt2(parent_node.point,rand3)
                new_node4=go_from_pt1_to_pt2(parent_node.point,rand4)
                node1=Node(new_node,parent_node)
                node2=Node(new_node2,parent_node)
                node3=Node(new_node3,parent_node)
                node4=Node(new_node4,parent_node)
                nodes.append(node1)
                nodes.append(node2)
                nodes.append(node3)
                nodes.append(node4)
                #print 'node1=',node1.point
                #print 'node2=',node2.point
                #print 'node3=',node3.point
                #print 'node4=',node4.point
                
                length_of_nodes=len(nodes)
                radius=50.0* math.sqrt((math.log(length_of_nodes)/length_of_nodes))
                
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
                    pygame.draw.line(screen,red,goal_node.point,goal_node.parent.point,3)
            else:
                print "out of nodes"
                return
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.image.save(screen,"rrt_gif.png")
                pygame.quit(); sys.exit()
                print 'points=',nodes.point


        pygame.display.update()

#fpsClock.tick(10)


if __name__== '__main__':
    main()


















