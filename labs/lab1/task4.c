int main()
{
    float a;
    float b;
    float c;
    float x;
    
    printf("a = ");
    scanf("%f", &a);
    printf("b = ");
    scanf("%f", &b);
    printf("c = ");
    scanf("%f", &c);
    
    x = (c - b) / a;
    printf("x=%f",x);
    return 0;
}
