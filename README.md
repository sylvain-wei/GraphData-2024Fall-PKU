# GraphData-2024Fall-PKU
北京大学2024Fall 海量图数据-邹磊-课程资料和作业

第一次作业：
1. 作业内容：任意实现下述两个子图同构算法中的一个。也可以选择复现其它论文的子图同构算法，但要求在实验报告中说明。
1) Ullmann Algroithm : 
    Relevant Publication:
    Julian R. Ullmann: An Algorithm for Subgraph Isomorphism.J. ACM 23(1): 31-42 (1976) .
2)  VF2 Algorithm:
    Relevant Publication:
    Luigi P. Cordella,Pasquale Foggia,Carlo Sansone,Mario Vento: A (Sub)Graph Isomorphism Algorithm for Matching Large Graphs.IEEE Trans. Pattern Anal. Mach. Intell. 26(10): 1367-1372 (2004)  
2. 提交内容：
1）程序源代码
2）实验报告（需包含算法的一些基本的性能分析，例如时间，空间消耗等）
3. 实验数据：
数据文件（包括查询文件Q系列和.data文件），每个文件都是多个图，图与图之间用 t开头的一行隔开（“t # i” 表示隔开第i-1个图和第i个图），每个图由多行（以v开头的是顶点行，以e开头的是边行）组成，“v i j” 表示图的顶点i的label是j，“e i j k” 表示图的边<i,j>的label是k。
数据下载： graphDB.zip （同上）
提交最后时间ddl： 11月1日