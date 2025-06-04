

%Lectura de datos
clc; close all; clear all;
root='directorio-archivo-espectro';
code='Si3N4\k2e';%cambiar
% 'SiI','ArII','ArI','N2','N2plus','OI'
root2='\UV_proc\';
% 'SiI','ArII','ArI','N2','N2plus'
A=load([root,code,root2,'1704146U2_cat_peaks_Areas2.dat']);
root2='\VIS_proc\';
% 'ArII','ArI','OI'
%a=load([root,code,root2,'1704147U2_cat_peaks.dat']);
B=load([root,code,root2,'1704147U2_cat_peaks_Areas2.dat']);
% Si3N4
Rangos=[245,275;
   958,988;
   1255,1285; 
   1640,1670;
   1997,2027;
   2176,2206;
   2354,2383;
   2680,2710;
   2977,3008;
   3482,3512;
   4165,4195];
% SiO2
% Rangos=[182,212;
%     330,360;
%     479,509;
%     717,746;
%     1281,1311;
%     1400,1429;
%     1696,1727;
%     1816,1846;
%     2054,2085];
% Si1/(Si1+Ar1) Ar1/(Ar1+Ar2)
% Uv
% Si1/(Si1+N2)
% Si1/(Si1+N2+)
Razones=[A(:,1)./(A(:,1)+B(:,2)),B(:,2)./(B(:,2)+B(:,1)),A(:,1)./(A(:,1)+A(:,4)),A(:,1)./(A(:,1)+A(:,5)),A(:,1)./(A(:,1)+B(:,3)), B(:,2)./(B(:,2)+B(:,3))];
% Vis
% Si1/(o1+Si1)
% ArI/(ArI+O1)
[signals,EigenFunciones,EigenValores]=pca1(Razones');
R=zeros(1,size(Razones,2));
Etiquetas=(1:size(Rangos,1));
%Saca promedios
for n=1:size(Rangos,1)
   x=Rangos(n,1):Rangos(n,2);
   R(n,:)=[mean(A(x,1))./mean(A(x,1)+B(x,2)),mean(B(x,2))./mean(B(x,2)+B(x,1)),mean(A(x,1))./mean(A(x,1)+A(x,4)),mean(A(x,1))./mean(A(x,1)+A(x,5)),mean(A(x,1))./mean(A(x,1)+B(x,3)), mean(B(x,2))./mean(B(x,2)+B(x,3))];
end
PCA=R*EigenFunciones;
plot(PCA(:,1),PCA(:,2),'*')
for k=1:9
   plot(PCA(k,1),PCA(k,2),'*')
   hold on
end
%leg={'1' '2'  '3' '4' '5' '6'};
%Nitruros
leg={'1' '2'  '3' '4' '5' '6' '7' '8' '9' '10' '11'};
%Oxidos
%leg={'1' '2'  '3' '4' '5' '6' '7' '8' '9'};
legend(leg) % outside loop
xlabel("PCA1")
ylabel("PCA2")
title(code);
%%
function [signals,PC,V] = pca1(data)
   % PCA1: Perform PCA using covariance.
   % data - MxN matrix of input data
   % (M dimensions, N trials)
   % signals - MxN matrix of projected data
   % PC - each column is a PC
   % V - Mx1 matrix of variances
   [M,N] = size(data);
   % subtract off the mean for each dimension
   mn = mean(data,2);
   data = data - repmat(mn,1,N);
   % calculate the covariance matrix
   covariance = 1 / (N-1) * data * data';
   % find the eigenvectors and eigenvalues
   [PC, V] = eig(covariance);
   % extract diagonal of matrix as vector
   V = diag(V);
   % sort the variances in decreasing order
   [junk, rindices] = sort(-1*V);
   V = V(rindices);
   PC = PC(:,rindices);
   % project the original data set
   signals = PC' * data;
end
