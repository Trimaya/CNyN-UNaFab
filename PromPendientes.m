

%Lectura de datos
clc; close all;
root='directorio-archivo-espectro';
code='L93';%cambiar
root2='\UV_proc\';
A=load([root,code,root2,'1704146U2_cat_peaks_Areas.dat']);
B=load([root,code,root2,'1704146U2_cat_peaks_Areas2.dat']);
%% Ajustar por mínimos cuadrados en una sola gráfica
Puntos=[50,25,20,15,10,5];
pendientes=zeros(size(B,1),size(B,2),size(Puntos,1));
for n=1:size(B,2) %para cada especie
   figure;
   for m=1:length(Puntos) %para la cantidad de puntos ajustados
       for k=1+Puntos(m):size(B,1) %Hace el trabajo
           X=k-Puntos(m):k;
           Y=B([k-Puntos(m):k],n);
           Z=polyfit(X,Y,1);
           pendientes(k,n,m)=Z(1);
       end
       plot(1:size(B,1),pendientes(:,n,m),'--','DisplayName',num2str(Puntos(m)))
%         n
%         Puntos(m)
%         mean(pendientes([400,700],n))
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
%% Calcula promedios para nitrógeno
% El orden de las especies en este experimento es
% 'SiI','ArII','ArI','N2','N2plus','OI'
n=3; %numero de especie para el nitrógeno
%para encontrar las pendientes es pendientes(rango, especie, elemento del vector puntos)
RangosAnalizar=[100,300;
   300,650;
   650,720;
   720,765;
   800,900;
   740,765];
for k=1:size(RangosAnalizar,1) 
   rango=RangosAnalizar(k,1):RangosAnalizar(k,2);
   for m=1:length(Puntos)
       PromEnRango(m)=mean(pendientes(rango, n,m));
       DesvEnRango(m)=std(pendientes(rango, n,m));
       IntConfianza([1,2],m)=[PromEnRango(m)-1.96*DesvEnRango(m)/sqrt(rango(end)-rango(1)),
           PromEnRango(m)+1.96*DesvEnRango(m)/sqrt(rango(end)-rango(1))];
       PromedioCero(m)=(IntConfianza(1,m)<=0) & (0<=IntConfianza(1,m));
   end
   disp('Rango:')
   [RangosAnalizar(k,1),RangosAnalizar(k,2)]
   disp('Puntos')
   Puntos
   disp('Promedios:')
   PromEnRango([1:length(Puntos)])
   disp('Desv:')
   DesvEnRango([1:length(Puntos)])
   disp('Int confianza')
   IntConfianza([1,2],[1:length(Puntos)])
   disp('Promedio en cero:')
   PromedioCero([1:length(Puntos)])
end
