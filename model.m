% PDE for American Call Options with Dividend Yield
%Parameters: Volatility, Interest Rate, Dividend Yield, Strike Price, Time
%to Expiry, Current Stock Price

price = linspace(50,150,100);

for i = 1:100
    OptionPrice(i) = AmericanPDE(0.16, 0.1,0.11,100,0.5,price(i));
    [Call(i),~] = blsprice(price(i),100,0.1,0.5,0.16);
end

figure
hold on
grid on
box on
plot(price,OptionPrice,'.')
plot(price,Call,'.')
xlabel('Stock price')
ylabel('Call Price')
legend("American Option","European Option")



function [OptionPrice] = AmericanPDE(sigma, r, q, K, tExpiry, STarget)


N = 252*10; %number of timesteps
dt = 1/N; %time division
%sigma = 0.16; %volatity
s_m = sigma * sqrt(2); %max volatity
%r = 0.1; %interest rate
%q = 0.11; %dividend yield
%K = 100; %Strike Price
time = 0:dt:1;
%Coefficients for PDE
p = (sigma^2) / (2*s_m^2);

mu = r - q - (sigma^2)/2;
p_u = p + 0.5* mu * sqrt(dt)/(2*s_m);
p_m = 1 - 2*p;
p_d = p - 0.5* mu * sqrt(dt)/s_m;


M = 5 * sqrt(N); %Max Option Price Range (can be changed)

Q = ceil(2 * M + 1); %Length of Stock Price Vector

%total  = p_d + p_m + p_u;

%initialize Stock Price, assuming exponential price behavior
S = ones(Q,1);
S(1) = 100 * exp(- M * s_m * sqrt(dt));

for i=2:Q
    S(i) = S(i - 1) * exp(s_m * sqrt(dt));
end

%initialize Call Price Vector
C = ones(N,Q); %American Call
C_e = ones(N,Q); %European Call

for i = 1:Q
    C(1,i) = max(S(i)-K,0);
    C_e(1,i) = max(S(i)-K,0);
end


for t = 2:N %Iterate Through Time
    for j = 2:(Q - 1) %Iterate Through Stock Price
        C(t,j) = p_u .* C(t-1,j+1) + p_m * C(t-1,j) + p_d .* C(t-1,j-1);
        C(t,j) = C(t,j) ./ (1 + r * dt);
        
        C_e(t,j) = p_u * C_e(t-1,j+1) + p_m * C_e(t-1,j) + p_d * C_e(t-1,j-1);
        C_e(t,j) = C_e(t,j) / (1 + r * dt);
    end
    
    %Zero Radiation Boundary Conditions
    %We can test different boundary conditions
    
    %C(t,Q) = p_u .* C(t-1,j-1) + p_m * C(t-1,j) + p_d .* C(t-1,j-1);
    %C(t,Q) = C(t,Q) ./ (1 + r * dt);
    
    C(t,1) = 0;
    C(t,Q) = C(1,Q);
    
    %C(t,1) = 2* C(t-1,2) - C(t-1,3);
    %C(t,Q) = 2* C(t-1,Q - 1) - C(t-1,Q - 2);
    
    for j=1:Q %American Call Option
        if C(t,j) < max(S(j)-K,0)
            C(t,j) = max(S(j)-K,0); %Ensures the option is >= Stock's intrinsic value
        end
    end
    
    % Identify the location and time for the price
    [~,indS] = min( abs(S-STarget) );
    [~,indT] = min( abs(time - tExpiry));
    OptionPrice = C(indT,indS);
    
end
end

% [X,Y] = meshgrid(S,0:dt:1);
% surf(X(1:end-1,:),Y(1:end-1,:),C)
% xlabel('Stock Price')
% ylabel('Time to Expiry')
% zlabel('Call Price')

