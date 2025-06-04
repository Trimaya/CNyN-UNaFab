

%% Normalized
NGauss = [];
NNumer = [];
for i=1:size(Numer,2)
   NNumer(:,i) = Numer(:,i)./mean(Numer(:,i));
end
for i=1:size(Gauss,2)
   NGauss(:,i) = Gauss(:,i)./mean(Gauss(:,i));
end
%% Simple substraction of normalized data
Subst = (Gauss-Numer)./Gauss;
Subst2 = (Gauss2-Numer2)./Gauss2;
figure;
hold on
title('Subst')
for i=1:size(Subst,2)
   plot(Subst(:,i))
end
legend(leg)
%% Doing histogram
figure;
set(gca,'fontname','Times New Roman')
title('Hist')
hold on
for i=1:size(Subst,2)
   histogram(Subst(:,i),'Normalization','probability','BinLimits',[-1,1],'BinWidth',0.05)
end
legend(leg)
%figure;
%tiledlayout("flow");
for i=1:size(Subst,2)
   %nexttile  
   figure;
   histogram(abs(Subst(:,i)),'Normalization','probability','BinLimits',[-1,1],'BinWidth',0.05,'FaceColor',colors(i,:))
   legend(leg(i))
   R = corrcoef(Numer(:,i),Gauss(:,i));
   %title(append(append('Hist ',leg(i),num2str(R(2,1)))))
   title(append(leg(i),' UV'))
   yticklabels(yticks*100)
   xticklabels(xticks*100)
   ylabel('Porcentaje de datos')
   xlabel('Diferencia')
   xlim([0,1])
   set(gcf,'Position',[0,0,800,500])
   fontsize(scale=1.75)
   set(gca,'fontname','Times New Roman')
end
%% For VIS
for i=1:size(Subst2,2)
   %nexttile
   figure;
   histogram(abs(Subst2(:,i)),'Normalization','probability','BinLimits',[-1,1],'BinWidth',0.05,'FaceColor',colors2(i,:))
   legend(leg2(i))
   R = corrcoef(Numer2(:,i),Gauss2(:,i));
   %title(append(append('Hist ',leg(i),num2str(R(2,1)))))
   title(append(leg2(i),' VIS'))
   ylabel('Proporcion de datos')
   xlabel('Diferencia proporcional')
   set(gcf,'Position',[0,0,800,500])
   yticklabels(yticks*100)
   xticklabels(xticks*100)
   ylabel('Porcentaje de datos')
   xlabel('Diferencia')
   xlim([0,1])
   fontsize(scale=1.75)
   set(gca,'fontname','Times New Roman')
end
