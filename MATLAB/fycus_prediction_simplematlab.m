%%% Prediction Fycus in normal Matlab
close all; clear all; clc
user     = 'universityofseville_zamorafernandez';   %insert-your-username-here';
password = '9paZ9sDlP2';       %insert-your-password-here';
lat   = 42.590317;
lon   = -5.64593;
start_date  = floor(now); % Could be anything like a datenum datenum(2016,12,24,12,3,2) <-> '2016-12-24T12:03:02Z';
start_date= datenum(2023, 04, 30, 12, 3, 2)
resolution  = 1/(24*10); % every 6 minutes
end_date    = start_date+2/24; % period of 2 hours from now
parameters='wind_speed_20000m:ms,wind_dir_20000m:d,air_density_20000m:kgm3';
[dn,data]=query_time_series_from_weather_api(user,password,start_date,resolution,end_date,parameters,lat,lon);
%% 
rho=data(:,3);
V_wind=data(:,1);
dir=deg2rad(data(:,2));
m=10; %mass of baloon (ask B2Space)
S_wet=200; %ask B2Space
Cd=0.05; %ask B2Space
Delta_t=5;% 5 seconds
for j=1:20 %1 hour prediction
for i=1:72 %180 times 5 seconds until the next prediction (each 15 minutes)
D(i,j)=1/2.*rho(j).*V_wind(j).^2.*S_wet.*Cd;
a(i,j)=D(i,j)/m; %ballon and cubesat moves with the wind
v(i,j)=V_wind(j);
traj(i,j)=V_wind(j)*Delta_t;
end
end

%%
x(1,1)=0; y(1,1)=0;
r=traj(:,1);
theta=dir;

for i=2:72 %only with firt prediction, still remains to update the solution each time a prediction of wind is taken
x(i)=r(i).*sin(theta(1))+x(i-1);
y(i)=r(i).*cos(theta(1))+y(i-1);

end
x_pc=x; %primera columna
y_pc=y;
figure
plot(x,y,'b.')
title('First 6 minutes trayectory of CubeSat')
xlabel('x-coordinate (m)')
ylabel('y coordinate (m)')
axes('pos',[.6 .7 .5 .3]) %[bottomleftcornerXposition bottomleftcornerYposition width height]
imshow('windrose.jpg')
 %% 
 X(:,1)=x_pc; Y(:,1)=y_pc;
r=traj;
theta=dir;
for j=2:20
    X(1,j)=X(72,j-1)+r(1,j).*sin(theta(j));
    Y(1,j)=Y(72,j-1)+r(1,j).*sin(theta(j));
for i=2:72 %only with firt prediction, still remains to update the solution each time a prediction of wind is taken
X(i,j)=r(i,j).*sin(theta(j))+X(i-1,j);
Y(i,j)=r(i,j).*cos(theta(j))+Y(i-1,j);

end
end

%Tranforming these matrixes to vectors in order to plot correctly
k=1; % vector index
for j=1:20
for i=1:72
    X_plot(k)=X(i,j);
    Y_plot(k)=Y(i,j);
    k=k+1;
end
end
figure

% windrose=imread('windrose.jpg');
% image([-0.5e4, 0] ,[0, 0.5e4], windrose); 
% hold on
plot(X_plot,Y_plot,'r.')
title('Predicted trayectory of CubeSat')
xlabel('x-coordinate (m)')
ylabel('y coordinate (m)')
axes('pos',[.6 .7 .5 .3]) %[bottomleftcornerXposition bottomleftcornerYposition width height]
imshow('windrose.jpg')

%%

%Tranforming these matrixes to vectors in order to plot correctly
k=1; % vector index
time=linspace(0,7200,72*20) %2 hours in seconds are 7200 seconds but with a time span of 5 seconds
for j=1:20
for i=1:72
    v_plot(k)=v(i,j);
    a_plot(k)=a(i,j);
    k=k+1;
end
end
figure
plot(time, v_plot, 'm.')
title('Velocity with respect to time')
xlabel('time (seconds)')
ylabel('velocity (m/s)')
plot(time, a_plot, 'm.')
title('Acceleration with respect to time')
xlabel('time (seconds)')
ylabel('acceleration (m/s^2)')

