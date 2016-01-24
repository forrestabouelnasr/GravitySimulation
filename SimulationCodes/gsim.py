def main(simulation_input):
    #a large collection of equal-mass stars interacts gravitationally
    G = simulation_input['G']
    n = simulation_input['n']
    pt = simulation_input['pt']
    t_final = simulation_input['t_final']
    m = simulation_input['m']
    v0 = simulation_input['v0']
    min_distance = simulation_input['min_distance']
    collision_distance = simulation_input['collision_distance']
    dt = simulation_input['dt']
    
    
    
    # initialize each star at a random point on a 2D grid, with random 2D velocity
    import random
    print( "initializing")
    coordinates=[]
    velocity=[]
    mass=[]
    display=[]
    v0=v0*(2**0.5)
    vx_total=0
    vy_total=0
    vz_total=0
    i=0
    min_distance_squared = min_distance ** 2
    total_number_of_frames=t_final/pt
    current_frame=0
    while i < n:
        coordinates.append([random.random(), random.random(), random.random()])
        velocity.append([v0*(random.random()-0.5), v0*(random.random()-0.5), v0*(random.random()-0.5)])
        vx_total+=velocity[i][0]
        vy_total+=velocity[i][1]
        vz_total+=velocity[i][2]
        i+=1
        mass.append(m);
        display.append(1);
    
    #enforce net zero momentum
    vx_average=vx_total/n
    vy_average=vy_total/n
    vz_average=vz_total/n
    i=0
    while i < n:
        velocity[i][0]-=vx_average
        velocity[i][1]-=vy_average
        velocity[i][2]-=vz_average
        i+=1
    
    def calculate_force(coordinates, G, m):
        force=[]
        closest_distance_squared=(coordinates[0][0]-coordinates[1][0])**2+(coordinates[1][0]-coordinates[1][1])**2+(coordinates[2][0]-coordinates[2][1])**2
        i=0
        while i < n:
            force.append([0,0,0])
            i+=1
        i=0
        while i < n-1:
            if mass[i]>0:
                j=i+1
                while j < n:
                    if mass[j]>0:
                        x_distance=coordinates[j][0]-coordinates[i][0]
                        y_distance=coordinates[j][1]-coordinates[i][1]
                        z_distance=coordinates[j][2]-coordinates[i][2]
                        distance_squared=x_distance**2 + y_distance**2 + z_distance**2
                        if closest_distance_squared > distance_squared:
                            closest_distance_squared = distance_squared
                        distance_squared = max(distance_squared, min_distance_squared)
                        distance = distance_squared ** 0.5
                        total_force= G * mass[i] * mass[j] / distance_squared
                        x_force = total_force * x_distance / distance
                        y_force = total_force * y_distance / distance
                        z_force = total_force * z_distance / distance
                        force[i][0] += x_force
                        force[i][1] += y_force
                        force[i][2] += z_force
                        force[j][0] -= x_force
                        force[j][1] -= y_force
                        force[j][2] -= z_force
                    j+=1
            i+=1
        #global dt
        #closest_distance_squared=max(closest_distance_squared,min_distance_squared)
        #dt = (closest_distance_squared**0.75)
        #if dt > pt:
        #    dt = pt/2;
        return force
    
    def update_velocity(force, velocity, dt):
        i=0
        while i < n:
            if mass[i]>0:
                velocity[i][0]+=force[i][0]*dt/mass[i]
                velocity[i][1]+=force[i][1]*dt/mass[i]
                velocity[i][2]+=force[i][2]*dt/mass[i]
            i+=1
        return velocity
    
    def update_coordinates(force, velocity, coordinates, dt, mass):
        i=0
        while i < n:
            if mass[i] > 0:
                coordinates[i][0]+=velocity[i][0]*dt+force[i][0]*dt*dt/mass[i]/2
                coordinates[i][1]+=velocity[i][1]*dt+force[i][1]*dt*dt/mass[i]/2
                coordinates[i][2]+=velocity[i][2]*dt+force[i][2]*dt*dt/mass[i]/2
            i+=1
        return coordinates
    
    def gather_report_for_printing(coordinates):
        string=''
        i=0
        while i < n:
            if display[i]==1:
                string=string+str(float(mass[i])**(1.0/3.0))+' '+str(coordinates[i][0])+' '+str(coordinates[i][1])+' '+str(coordinates[i][2])+' '
            i+=1
        string=string+'\n'
        return string
    
    def collide(coordinates,velocity):
        i=0
        while i < n-1:
            j=i+1
            while j < n:
                if mass[i]*mass[j]>0:
                    x_distance=coordinates[j][0]-coordinates[i][0]
                    y_distance=coordinates[j][1]-coordinates[i][1]
                    z_distance=coordinates[j][2]-coordinates[i][2]
                    distance_squared=x_distance**2 + y_distance**2 + z_distance**2
                    if distance_squared < collision_distance:
                        velocity[i][0]=(velocity[i][0]*mass[i]+velocity[j][0]*mass[j])/(mass[i]+mass[j])
                        velocity[i][1]=(velocity[i][1]*mass[i]+velocity[j][1]*mass[j])/(mass[i]+mass[j])
                        velocity[i][2]=(velocity[i][2]*mass[i]+velocity[j][2]*mass[j])/(mass[i]+mass[j])
                        coordinates[i][0]=(coordinates[i][0]*mass[i]+coordinates[j][0]*mass[j])/(mass[i]+mass[j])
                        coordinates[i][1]=(coordinates[i][1]*mass[i]+coordinates[j][1]*mass[j])/(mass[i]+mass[j])
                        coordinates[i][2]=(coordinates[i][2]*mass[i]+coordinates[j][2]*mass[j])/(mass[i]+mass[j])
                        mass[i]=mass[i]+mass[j]
                        mass[j]=0
                        velocity[j][0]=0;
                        velocity[j][1]=0;
                        velocity[j][2]=0;
                        display[j]=0;
                j+=1
            i+=1
        return coordinates, velocity
    
    print( "starting simulation")
    t=0
    latest_printed=0;
    force = calculate_force(coordinates, G, m)
    file = open('coordinates_output', 'w')
    while t < t_final:
        force = calculate_force(coordinates, G, m)
        velocity = update_velocity(force, velocity, dt)
        coordinates = update_coordinates(force, velocity, coordinates, dt, mass)
        coordinates,velocity = collide(coordinates,velocity)
        t+=dt
        while t-latest_printed>=pt:
            coordinates_string = gather_report_for_printing(coordinates)
            file.write(coordinates_string)
            current_frame+=1
            print (str(current_frame)+"/"+str(total_number_of_frames)+" complete")
            latest_printed+=pt
        
    file.close()
    print ('finished with simulation')
    
    from visualize import make_gif
    make_gif()

