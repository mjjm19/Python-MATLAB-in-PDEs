% Jeffcott Rotor: Bode, Orbit, Transient response
% I used simplified anisotrophy model (different kx ky) to capture the basic effect on 
orbit shape. 
% This code implements a Jeffcott rotor model to study the funadamental rotor dynamic behavior. 
% Using Runge-Kutta ODE solver (ODE45) we capture critical speed resonance, orbit motion, anisotropic ebaring effects and transient run-up response.


clear; clc; close all;

% Parameters 

m = 5.0;                 % kg
fn = 100;                % target natural freq [Hz]
k = (2*pi*fn)^2 * m;     % N/m
zeta = 0.02;             % damping ratio
c = 2*zeta*sqrt(k*m);    % N s/m
e = 5e-4;                % m (eccentricity)
rpm2rad = 2*pi/60;

% Bode via steady-state ODE

rpms = linspace(300,9000,120);
Apeak = zeros(size(rpms));

for i=1:numel(rpms)
    om = rpms(i)*rpm2rad;
    % State X=[x vx y vy]
    f = @(t,X)[ X(2);
                (m*e*om^2*cos(om*t) - c*X(2) - k*X(1))/m;
                X(4);
                (m*e*om^2*sin(om*t) - c*X(4) - k*X(3))/m ];
    % let transients die
    [~,X] = ode45(f,[0 1.5],[0 0 0 0]);
    % sample steady part
    [~,Xs] = ode45(f,[0 1.5],X(end,:));
    amp = sqrt(Xs(:,1).^2 + Xs(:,3).^2);
    Apeak(i) = max(amp(end-round(0.3*length(amp)):end));
end

% Detecting critical speed (peak)

[~,idx] = max(Apeak); crit_rpm = rpms(idx);

figure; plot(rpms, Apeak, 'LineWidth',1.5);
hold on; yline(Apeak(idx),'--'); xline(crit_rpm,'--');
xlabel('Speed [rpm]'); ylabel('Amplitude [m]');
title('Bode (peak amplitude vs speed)');
grid on;

% Orbit at selected speed

rpm_view = crit_rpm;    % try below/near/above
om = rpm_view*rpm2rad;
f = @(t,X)[ X(2);
            (m*e*om^2*cos(om*t) - c*X(2) - k*X(1))/m;
            X(4);
            (m*e*om^2*sin(om*t) - c*X(4) - k*X(3))/m ];
[~,X] = ode45(f,[0 1.5],[0 0 0 0]);      % kill transient
[t2,X2] = ode45(f,[0 0.5],X(end,:));     % capture steady
x = X2(:,1); y = X2(:,3);

figure; plot(x,y,'LineWidth',1.5); axis equal; grid on;
xlabel('x [m]'); ylabel('y [m]');
title(sprintf('Orbit at %.0f rpm', rpm_view));

% Bearing effects (anisotropic)

kx = 1.2*k; ky = 0.8*k; cx = c; cy = c;  % simplified anisotropy
om = crit_rpm*rpm2rad;
f_aniso = @(t,X)[ X(2);
                  (m*e*om^2*cos(om*t) - cx*X(2) - kx*X(1))/m;
                  X(4);
                  (m*e*om^2*sin(om*t) - cy*X(4) - ky*X(3))/m ];
[~,X] = ode45(f_aniso,[0 1.5],[0 0 0 0]);
[~,X2] = ode45(f_aniso,[0 0.5],X(end,:));
xa = X2(:,1); ya = X2(:,3);
figure; plot(xa,ya,'LineWidth',1.5); axis equal; grid on;
xlabel('x [m]'); ylabel('y [m]');
title('Orbit with anisotropic bearings (k_x ≠ k_y)');

% Transient response 

tend = 6; om0 = 300*rpm2rad; om1 = 9000*rpm2rad;
om_t = @(t) om0 + (om1-om0)*t/tend;
fr = @(t,X)[ X(2);
             (m*e*om_t(t)^2*cos(om_t(t)*t) - c*X(2) - k*X(1))/m;
             X(4);
             (m*e*om_t(t)^2*sin(om_t(t)*t) - c*X(4) - k*X(3))/m ];
[tt,XR] = ode45(fr,[0 tend],[0 0 0 0]);
amp = sqrt(XR(:,1).^2 + XR(:,3).^2);
rpm_run = om_t(tt)/rpm2rad;

figure; plot(rpm_run,amp,'LineWidth',1.2); grid on;
xlabel('Speed [rpm]'); ylabel('Amplitude [m]');
title('Run-up amplitude vs speed');
