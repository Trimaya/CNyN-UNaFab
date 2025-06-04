

%Pendiente de la integral
clc; close all;
root='directorio-archivo-espectro\';
code='L93';%cambiar
root2='\UV_proc\';
A=load([root,code,root2,'1704146U2_cat_peaks_Areas.dat']);
B=load([root,code,root2,'1704146U2_cat_peaks_Areas2.dat']);
%% Ajustar por mínimos cuadrados en una sola gráfica
Puntos=[50,25,20,15];
pendientes=zeros(size(B,1),size(B,2),size(Puntos,1));
for n=1:size(B,2) %para cada especie
   figure;
   for m=1:length(Puntos) %para la cantidad de puntos ajustados
       for k=1+Puntos(m):size(B,1) %Hace el trabajo
           X=k-Puntos(m):k;
           Y=B([k-Puntos(m):k],n);
           Z=polyfit(X,Y,1);
           pendientes(k,n)=Z(1);
       end
       plot(1:size(B,1),pendientes(:,n),'--','DisplayName',num2str(Puntos(m)))
       n
       Puntos(m)
       mean(pendientes([400,700],n))
       hold on   
   end
   X=1:size(B,1);
   Y=B(:,n)';
   Z=zeros(size(Y));
   Z(2:end)=diff(Y)/diff(X);
   plot(X,Z,'--','DisplayName','Derivada')
   title(['especie ',num2str(n)])
   xlabel('número de archivo')
   ylabel('pendiente')
   legend;
end
%% Ajustar por mínimos cuadrados en diferentes subplots
Puntos=[50,25,20,15,10,5];
pendientes=zeros(size(B,1),size(B,2),size(Puntos,1));
for n=1:size(B,2)
   figure;
   title(['especie ',num2str(n)])
   for m=1:length(Puntos)
       for k=1+Puntos(m):size(B,1)
           X=k-Puntos(m):k;
           Y=B([k-Puntos(m):k],n);
           Z=polyfit(X,Y,1);
           pendientes(k,n)=Z(1);
       end
       subplot(2,4,m)
       plot(1:size(B,1),pendientes(:,n),'--','DisplayName',num2str(Puntos(m)))
       legend  
   end
   X=1:size(B,1);
   Y=B(:,n)';
   Z=zeros(size(Y));
   Z(2:end)=diff(Y)/diff(X);
   subplot(2,4,length(Puntos)+1)
   plot(X,Z,'--','DisplayName','Derivada')
   xlabel('número de archivo')
   ylabel('pendiente')
   legend;
end
