

%%
% Import data manually
close all;
Gauss = double(UVAreas1{:,:}); %UVAreas1 = UV de nitruro de silicio
Numer = double(UVAreas2{:,:});
Gauss2 = double(VISAreas1{:,:});
Numer2 = double(VISAreas2{:,:});
X = linspace(0,size(Gauss,1),size(Gauss,1));
X2 = linspace(0,size(Gauss2,1),size(Gauss2,1));
X = X.*2;
X2 = X2.*2;
leg = [{'SiI'},{'ArII'},{'ArI'},{'N2'},{'N2+'},{'O'}];
leg2 = [{'ArII'},{'ArI'},{'O'}];
colors = [[0 0.4470 0.7410];[0.8500 0.3250 0.0980];[0.9290 0.6940 0.1250];[0.4940 0.1840 0.5560];[0.4660 0.6740 0.1880];[0.3010 0.7450 0.9330];[0.6350 0.0780 0.1840]];
colors2 = [colors(2,:);colors(3,:);colors(6,:)];
%% Raw Plots
lw = 1;
pos = [-0.12,1];
figure;
set(gcf,'color','w');
set(gcf,'position',[0,0,[1300,500]]);
tiledlayout(2,2,'TileSpacing','compact')
nexttile(1)
hold on
%GaussUV
title('a)', 'Position', pos, 'Units', 'normalized' , 'VerticalAlignment', 'top', 'HorizontalAlignment', 'center','FontSize',14,'FontWeight','bold')
for i=1:size(Gauss,2)
   plot(X,Gauss(:,i),LineWidth=lw)
end
xticklabels([])
legend(leg)
set(gca,'fontname','Times New Roman')
xlim("tight")
ylim("tickaligned")
ylabel('Intensidad [U.A.]')
nexttile(3)
hold on
%NumerUV
title('c)', 'Position', pos, 'Units', 'normalized' , 'VerticalAlignment', 'top', 'HorizontalAlignment', 'center','FontSize',14,'FontWeight','bold')
for i=1:size(Numer,2)
   plot(X,Numer(:,i),LineWidth=lw)
end
plot(X(1,1),Numer(1,1),LineWidth=lw) %hack for adding to legend
legend(leg)
set(gca,'fontname','Times New Roman')
xlim("tight")
ylim("tickaligned")
xlabel('Tiempo [s]')
ylabel('Intensidad [U.A.]')
nexttile(2)
hold on
%GaussVIS
title('b)', 'Position', pos, 'Units', 'normalized' , 'VerticalAlignment', 'top', 'HorizontalAlignment', 'center','FontSize',14,'FontWeight','bold')
for i=1:size(Gauss2,2)
   plot(X2,Gauss2(:,i),"Color",colors2(i,:),LineWidth=lw)
end
xticklabels([])
legend(leg2)
set(gca,'fontname','Times New Roman')
xlim("tight")
ylim("tickaligned")
ylabel('Intensidad [U.A.]')
set(gca, 'YScale', 'log')
nexttile(4)
hold on
%NumerVIS
title('d)', 'Position', pos, 'Units', 'normalized' , 'VerticalAlignment', 'top', 'HorizontalAlignment', 'center','FontSize',14,'FontWeight','bold')
for i=1:size(Numer2,2)
   plot(X2,abs(Numer2(:,i)),"Color",colors2(i,:),LineWidth=lw) %abs to fix one negative point in data
end
legend(leg2)
set(gca,'fontname','Times New Roman')
xlim("tight")
ylim("tickaligned")
ylabel('Intensidad [U.A.]')
xlabel('Tiempo [s]')
set(gca, 'YScale', 'log')
