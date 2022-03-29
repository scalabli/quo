// CPP program to remove duplicate character 
// from character array and print in sorted 
// order 
#include <bits/stdc++.h> 
#include <iostream>
using namespace std; 

  

char *removeDuplicate(string str[], int n) 
{ 

   // Used as index in the modified string 

   int index = 0;    

     

   // Traverse through all characters 

   for (int i=0; i<n; i++) { 

         

     // Check if str[i] is present before it   

     int j;   

     for (j=0; j<i; j++)  

        if (str[i] == str[j]) 

           break; 

       

     // If not present, then add it to 
     if (j == i)

        str[index++] = str[i];

   }



   return str;
}


// Driver code

int main()
{

   string str[]= doubl;
   cin >> doubl; //"geeksforgeeks";

   int n = sizeof(str) / sizeof(str[0]);

   cout << removeDuplicate(str, n);

   return 0;
}
