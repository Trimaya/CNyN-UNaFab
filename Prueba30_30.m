

%%Lectura de datos
clc; close all; clear all;
%root='directorio';
%code='L93';%cambiar
%% UV
%root2='\UV_proc\';
A=load(['UVAreas1.dat']);
B=load(['UVAreas2.dat']);
%% Ajustar por mínimos cuadrados en una sola gráfica
Puntos=[50,25,20,15,10,5];
pendientes=zeros(size(B,1),size(B,2),size(Puntos,1));
Especies=[{'SiI'},{'ArII'},{'ArI'},{'N2'},{'N2+'}];
numEsp=1;
for n=1:size(B,2) %para cada especie
   figure;
   for m=1:length(Puntos) %para la cantidad de puntos ajustados
       for k=1+Puntos(m):size(B,1) %Hace el trabajo
           X=k-Puntos(m):k;
           Y=B(k-Puntos(m):k,n);
           Z=polyfit(X,Y,1);
           pendientes(k,n,m)=Z(1);
       end
       plot(1:size(B,1),pendientes(:,n,m),'--','DisplayName',num2str(Puntos(m)))
       hold on   
   end
   title(Especies(numEsp));
   numEsp=numEsp+1;
end
%% Calcula promedios para nitrógeno
% el orden de las especies en este experimento es
% 'SiI','ArII','ArI','N2','N2plus','OI'
%para encontrar las pendientes es pendientes(rango, especie, elemento del vector puntos)
% Prueba de 30 en 30
close all
n=[1,4,5]; %numero de especie para el nitrógeno
Ventana=30;%>0
IniciaEn=1;%1 o mas
TerminaEn=1500;
PuntosEstabilidad=30;
X=IniciaEn+Ventana-1:TerminaEn;
Z=1.96;%dependiente del coeficiente de confianza [0.90,1.645;0.95,1.96;0.98,2.33;0.99,2.58]
Contador=zeros(length(n),length(Puntos));
EstableEn=zeros(length(Puntos),length(X),length(n));
%ii=0;
for k=X
   rango=k-Ventana+1:k;
   for numElemento=1:length(n)
       for m=1:length(Puntos)
           PromEnRango(m,k-X(1)+1,numElemento)=mean(pendientes(rango, n(numElemento), m));
           DesvEnRango(m,k-X(1)+1,numElemento)=std(pendientes(rango, n(numElemento), m));
           IntConfianza(m,k-X(1)+1,numElemento)=Z*DesvEnRango(m,k-X(1)+1,numElemento)/sqrt(30);
           PromedioCero(m,k-X(1)+1,numElemento)=(PromEnRango(m,k-X(1)+1,numElemento)-IntConfianza(m,k-X(1)+1,numElemento)<=0) & (0<=PromEnRango(m,k-X(1)+1,numElemento)+IntConfianza(m,k-X(1)+1,numElemento));
           if PromedioCero(m,k-X(1)+1,numElemento)
               Contador(numElemento,m)=Contador(numElemento,m)+1;
           else
               Contador(numElemento,m)=0;
           end
           if Contador(numElemento,m)==PuntosEstabilidad
               EstableEn(m,k-X(1)+1,numElemento)=1;
               Contador(numElemento,m)=Contador(numElemento,m)-1;
           end
       end
   end
end
for numElemento=1:length(n)
   figure;
   sgtitle(["Estabilidad ventana", Especies(n(numElemento))])
   for m=1:length(Puntos)
       subplot(2,3,m)
       plot(X,PromedioCero(m,:,numElemento));
       title(Puntos(m))
       ylim([0,1.05]);
   end
   figure;
   sgtitle(["Establidad plasma", Especies(n(numElemento))])
   for m=1:length(Puntos)
       subplot(2,3,m)
       plot(X,EstableEn(m,:,numElemento));
       title(Puntos(m))
       ylim([0,1.05]);
   end
end
EstabilidadTotal=EstableEn(:,:,1)*0;
Resultados=zeros(length(Puntos),size(EstableEn,2));
for m=1:length(Puntos)
   for numElemento=1:length(n)
       EstabilidadTotal(m,:)=EstabilidadTotal(m,:)+EstableEn(m,:,numElemento);
   end
end
Resultados=EstabilidadTotal==length(n);
%%
EstabilidadFinal=EstableEn*0;
EstabilidadFinal=cat(3,EstabilidadFinal,EstabilidadFinal);
for m=1:length(Puntos)
   %figure;
   %hold on;
   for numElemento=1:length(n)
       %title(['Estabilidad del plasma: ' num2str(Puntos(m)) ' puntos']);
       %plot(X, double(EstableEn(m,:,numElemento)) + numElemento*1.2 - 1);
       EstabilidadFinal(m,:,numElemento)=double(EstableEn(m,:,numElemento)) + 6 - (numElemento-1) - 0.2*(numElemento-1);
   end
end
%% Vis
clear PromPendientes pendientes PromEnRango IntConfianza DesvEnRango
%root2='\Vis_proc\';
A=load(['VISAreas1.dat']);
B=load(['VISAreas2.dat']);
%% Ajustar por mínimos cuadrados en una sola gráfica
Puntos=[50,25,20,15,10,5];
pendientes=zeros(size(B,1),size(B,2),size(Puntos,1));
Especies=[{'ArII'},{'ArI'},{'OI'}];
numEsp=1;
for n=1:size(B,2) %para cada especie
   figure;
   for m=1:length(Puntos) %para la cantidad de puntos ajustados
       for k=1+Puntos(m):size(B,1) %Hace el trabajo
           X=k-Puntos(m):k;
           Y=B(k-Puntos(m):k,n);
           Z=polyfit(X,Y,1);
           pendientes(k,n,m)=Z(1);
       end
       plot(1:size(B,1),pendientes(:,n,m),'--','DisplayName',num2str(Puntos(m)))
       hold on   
   end
   title(Especies(numEsp));
   numEsp=numEsp+1;
end
%% Calcula promedios para nitrógeno
% el orden de las especies en este experimento es
% 'SiI','ArII','ArI','N2','N2plus','OI'
%para encontrar las pendientes es pendientes(rango, especie, elemento del vector puntos)
% Prueba de 30 en 30
n=[1,2,3]; %numero de especie para el nitrógeno
Ventana=30;%>0
IniciaEn=1;%1 o mas
TerminaEn=1500;
PuntosEstabilidad=30;
X=IniciaEn+Ventana-1:TerminaEn;
Z=1.96;%dependiente del coeficiente de confianza [0.90,1.645;0.95,1.96;0.98,2.33;0.99,2.58]
Contador=zeros(length(n),length(Puntos));
EstableEn=zeros(length(Puntos),length(X),length(n));
%ii=0;
for k=X
   rango=k-Ventana+1:k;
   for numElemento=1:length(n)
       for m=1:length(Puntos)
           PromEnRango(m,k-X(1)+1,numElemento)=mean(pendientes(rango, n(numElemento), m));
           DesvEnRango(m,k-X(1)+1,numElemento)=std(pendientes(rango, n(numElemento), m));
           IntConfianza(m,k-X(1)+1,numElemento)=Z*DesvEnRango(m,k-X(1)+1,numElemento)/sqrt(30);
           PromedioCero(m,k-X(1)+1,numElemento)=(PromEnRango(m,k-X(1)+1,numElemento)-IntConfianza(m,k-X(1)+1,numElemento)<=0) & (0<=PromEnRango(m,k-X(1)+1,numElemento)+IntConfianza(m,k-X(1)+1,numElemento));
           if PromedioCero(m,k-X(1)+1,numElemento)
               Contador(numElemento,m)=Contador(numElemento,m)+1;
           else
               Contador(numElemento,m)=0;
           end
           if Contador(numElemento,m)==PuntosEstabilidad
               EstableEn(m,k-X(1)+1,numElemento)=1;
               Contador(numElemento,m)=Contador(numElemento,m)-1;
           end
       end
   end
end
for numElemento=1:length(n)
   figure;
   sgtitle(["Estabilidad ventana", Especies(n(numElemento))])
   for m=1:length(Puntos)
       subplot(2,3,m)
       plot(X,PromedioCero(m,:,numElemento));
       title(Puntos(m))
       ylim([0,1.05]);
   end
   figure;
   sgtitle(["Establidad plasma", Especies(n(numElemento))])
   for m=1:length(Puntos)
       subplot(2,3,m)
       plot(X,EstableEn(m,:,numElemento));
       title(Puntos(m))
       ylim([0,1.05]);
   end
end
Resultados2=EstabilidadTotal==length(n);
Resultados3=Resultados+Resultados2;
Resultados3=Resultados3==2;
figure
sgtitle(["Intersección Z=",num2str(Z)])
for m=1:length(Puntos)
   subplot(2,3,m)
   plot(X,Resultados3(m,:));
   title(Puntos(m));
   ylim([0,1.05])
end
%%
for m=1:length(Puntos)
   %figure;
   %hold on;
   for numElemento=1:length(n)
       title(['Estabilidad del plasma: ' num2str(Puntos(m)) ' puntos']);
       plot(X, double(EstableEn(m,:,numElemento)) + numElemento*1.2 - 1);
       EstabilidadFinal(m,:,numElemento+3)=double(EstableEn(m,:,numElemento)) + 6 - (numElemento-1+3) - 0.2*(numElemento-1+3);
   end
end
%%
DAN=flip(linspace(0,size(EstabilidadFinal,3)-1,size(EstabilidadFinal,3)));
for m=1:length(Puntos)
   for numElemento=1:size(EstabilidadFinal,3)
       EstabilidadFinal2(m,:,numElemento) = EstabilidadFinal(m,:,numElemento) - DAN(numElemento)*1.2*ones(1,size(EstabilidadFinal,2)) + 0*ones(1,size(EstabilidadFinal,2));
   end
end
for m=1:length(Puntos)
   for numElemento=1:size(EstabilidadFinal,3)
       EstabilidadFinal2(m,:,numElemento) = 1.0*(EstabilidadFinal2(m,:,numElemento) + 1.1*(numElemento-1)*ones(1,size(EstabilidadFinal,2)));
   end
end
%%
letters = ["a)",'b)','c)','d)','e)','f)','g)'];
%close all;
DAN = linspace(0,size(EstabilidadFinal,3)-1,size(EstabilidadFinal,3));
tiledlayout(3,2,'TileSpacing','compact')
for m=1:length(Puntos)
   %figure;
   nexttile;
   set(gcf,'color','w');
   set(gca, 'FontName', 'Times New Roman')
   hold on;
   colors=[[0 0.4470 0.7410];[0.8500 0.3250 0.0980];[0.9290 0.6940 0.1250];[0.4940 0.1840 0.5560];[0.4660 0.6740 0.1880];[0.3010 0.7450 0.9330]];
   for numElemento=1:size(EstabilidadFinal2,3)
       %title(['Estabilidad : ' num2str(Puntos(m)) ' puntos']);
       title(letters(m), 'Position', [-0.1,1], 'Units', 'normalized' , 'VerticalAlignment', 'top', 'HorizontalAlignment', 'center','FontSize',14,'FontWeight','bold')
       minval = min(EstabilidadFinal2(m,:,numElemento));
       patch([X(1),X,X(end)],[min(EstabilidadFinal2(m,:,numElemento)),EstabilidadFinal2(m,:,numElemento),min(EstabilidadFinal2(m,:,numElemento))],colors(numElemento,:));
       ylim([-0.2,7.4])
       xlim([X(1),X(end)*1])
   end
   yticks([0.5 1.6 2.7 3.8 4.9 6.0])
   yticklabels([])
   %yticklabels({'\color[rgb]{0 0.4470 0.7410}SiI','\color[rgb]{0.8500 0.3250 0.0980}ArII','\color[rgb]{0.9290 0.6940 0.1250}ArI','\color[rgb]{0.4940 0.1840 0.5560}N2','\color[rgb]{0.4660 0.6740 0.1880}N2+','\color[rgb]{0.3010 0.7450 0.9330}OI'})
   ylim([-0.1,6.7])
   xticks([0:250:1500])
   xlim([0,1500])
   xticklabels([])
   if m == 5 | m == 6
       %xticklabels({'0','','','','','5','','','','','10','','','','','15','','','','','20','','','','','25','','','','','30','','','','','35','','','','','40','','','','','45','','','','','50'})
       xticklabels({'0','500','1000','1500','2000','2500','3000'})
       xlabel('tiempo [s]')
   end
  
   set(gcf,'position',[10,10,[1500,400]]);
end
plots=get(gca, 'Children');
[~, objh]=legend(plots,flip([{'SiI'},{'N2'},{'N2+'},{'ArII'},{'ArI'},{'OI'}]))
objhl = findobj(objh, 'type', 'line');
set(objhl, 'Markersize', 1000);
