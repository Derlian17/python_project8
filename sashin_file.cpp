#include <iostream>
#include <fstream>
using namespace std;

int main(){
    int line;
    char mass[100];
    ifstream fin;
    ofstream fout;
    fout.open("sdkj.txt");
    fout <<20<<endl<<458<<endl<<3489<<endl<<532<<endl<<-684899;
    fout.close();
	fin.open("sdkj.txt");
    while (!fin.eof()){
        fin.getline(mass,20);
        line+=1;
        }
	int i = 4;
	cout<<endl;
    while (mass[i]){
    	
    	cout<<mass[i];
    	i++;
	}
}