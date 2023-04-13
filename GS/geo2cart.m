function [x,y,z]=geo2cart(h,phi,lambda)
%This function transforms geodesian to cartesian earth-centered coordinates
%Geodesian coordinates must be given in radians.

%Definition of ellipsoidal Earth model WGS-84 (used for GPS)
phi=phi*pi/180;
lambda=lambda*pi/180;

f=1/298.257224; %
re=6378.137*1e3;

x=(h+re/sqrt(1-f*(2-f)*sin(phi)^2))*cos(phi)*cos(lambda);
y=(h+re/sqrt(1-f*(2-f)*sin(phi)^2))*cos(phi)*sin(lambda);
z=(h+(re*(1-f)^2)/sqrt(1-f*(2-f)*sin(phi)^2))*sin(phi);
end