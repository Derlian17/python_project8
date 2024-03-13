
#include <iostream>
#include <fstream>
#include <math.h>
using namespace std;
//Размеры дрона:
#define DRONH 1   //высота дрона
#define DRONW 2.5 //ширина дрона
#define DRONL 3   //длина дрона

// координаты {OX, OY, OZ}
int dron_coord[3]={0,0,0};
int end_coord[3]={0,70,0};
int dron_degr=0;
int past_dist=0, dist=0;
/*
АЛГОРИТМ:

пока нет препятствия
    вычеслить кротчайший путь, осмотреться, идти
если  в препятствии есть дырень под дрон || препятствие можно обойти сразу
    если ничего не мешает обойти
        обойти
    иначе
        цикл
            ползти в ту сторону, что приближает к концу
            если  со стороны препятствия что-то изменилось   выйти из цикла
            //(пока нету)если  ползём как-то долго, то возвращаемся обратно и ползём в другую сторону


*/
int main(){
    Round(0); //чтобы получить первое показание с датчика
    for(;;){
        while (dist==-1||dist>3){
            if(It_is_finish()){return;}
            Round(Shortest_route()-dron_degr);
            if(Something_is_in_the_way()){break;}
            Step(1);
            }
        Look_around();
    }
}

//-------------------------------------------------------------------------------------------------------
void Step(int x){ //не танец, а конфетка
    dron_coord[0]+=x*sin(dron_degr);
    dron_coord[1]+=x*cos(dron_degr);
    ofstream file;
    file.open("log.txt");
    file<<"B move("<<x<<")";
    file.close();
    Find_dist();
}
//-------------------------------------------------------------------------------------------------------
void Round(int x){ //поворот
    dron_degr+=x;
    ofstream file;
    file.open("log.txt");
    file<<"B rotate("<<x<<")";
    file.close();
    Find_dist();
}
//-------------------------------------------------------------------------------------------------------
void Find_dist(){
    past_dist=dist;
    char mass[10];
    ifstream fin;
    fin.open("log.txt");
    while (!fin.eof()){
        fin.getline(mass,20);
    }
    dist=0;
    int r, i=0;
    while (mass[i]){
    	r=mass[i]-'0';
    	dist=(dist*10)+r;
        i++;
    }
    fin.close();
}
//-------------------------------------------------------------------------------------------------------
int Something_is_in_the_way(){
    Round(5);
    Round(-10);
    if(dist==-1||past_dist==-1){Round(5);return 0;}
    else{Round(5);return 1;}
}
//-------------------------------------------------------------------------------------------------------
void Look_around(){ //Хочешь жить? Умей вертеться
    int degr=0;
    while (degr<=90)
    { //поворот влево
        degr+=5;
        Round(5);
        if(dist==-1){Bypass(degr, past_dist);return;}
        if(dist>(sin(degr)*dist)){ //если обнаружена пустота
            if((sin(degr)*dist) - (sin(degr-1)*past_dist) > DRONW) {Go_around(degr); return;} //проверяем войдёт ли корпус
        }
    }
    Round(-1*degr);
    degr=0;
    while (degr>=-90)
    { //поворот вправо
        degr-=5;
        Round(-5);
        if(dist==-1){Bypass(degr, past_dist);return;}
        if(dist>(sin(-degr)*dist)) //если обнаружена пустота
            {if((sin(-degr)*dist) - (sin(1-degr)*past_dist) > DRONW){Go_around(degr); return;} //проверяем войдёт ли корпус
            }
    }
}
//-------------------------------------------------------------------------------------------------------
void Go_around(int degr){ //в пространство между препятсвиями
    if(degr>0){
        Round(90-degr);
        if(dist==-1){Step((sin(degr-1)*past_dist)+0.5*DRONW);}
        else{Round(-90);Adjust();}
    }else{
        Round(-90-degr);
        if(dist==-1){Step((sin(degr-1)*past_dist)+0.5*DRONW);}
        else{Round(90);Adjust();}
        }
}
//-------------------------------------------------------------------------------------------------------
void Bypass(int degr, int rasst){ //Обойти препятсвие, когда ничего не мешает(когда не танцор)
    if(degr>0){
        Round(90-degr);
        if(dist==-1){Step((sin(degr-1)*rasst)+0.5*DRONW);}
        else{Round(-90);Adjust();}
    }else{
        Round(-90-degr);
        if(dist==-1){Step((sin(degr-1)*rasst)+0.5*DRONW);}
        else{Round(90);Adjust();}
        }
}
//-------------------------------------------------------------------------------------------------------
int Shortest_route(){ //Путь подскажет к точке конечной (м. йода)
    if(dron_coord[0]>0){
        return -1*atan((abs(dron_coord[0]-end_coord[0]))/(abs(dron_coord[1]-end_coord[1])));
        }else{
            return atan((abs(dron_coord[0]-end_coord[0]))/(abs(dron_coord[1]-end_coord[1])));}
}
//-------------------------------------------------------------------------------------------------------
void Adjust(){ //подстроиться под пл-ть
    int degr, otr;
    Round(10); //отклонямся чтобы узнать расстояние
    otr = sgrt((dist*dist)+(past_dist*past_dist)-2*dist*past_dist*cos(10)); //находим неизвестный отрезок по т.косинусов
    degr = 180-(acos(((otr*otr)+(past_dist*past_dist)-(dist*dist))/(2*otr*past_dist))); //находим угол смежный углу между преждней дистанцией и найденным отрезком по т.косинусов
    if(dist<=past_dist){degr=degr*(-1);}
    Round(-10); //на исходную
    while(dist!=-1||dist>=4){ //ползти вдоль
        Round(degr); //повернулись параллельно препятствию
        Step(0.5); //идём
        Round(-degr); //смотрим на препятствие
    }
}
//-------------------------------------------------------------------------------------------------------
int It_is_finish(){
    if((abs(dron_coord[0]-end_coord[0])<=2)&&(abs(dron_coord[1]-end_coord[1])<=2)&&(abs(dron_coord[2]-end_coord[2])<=2)){return 1;}
    else{return 0;}
}
//-------------------------------------------------------------------------------------------------------