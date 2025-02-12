'''
https://leetcode.cn/problems/cat-and-mouse/description/
两位玩家分别扮演猫和老鼠，在一张 无向 图上进行游戏，两人轮流行动。

图的形式是：graph[a] 是一个列表，由满足 ab 是图中的一条边的所有节点 b 组成。

老鼠从节点 1 开始，第一个出发；猫从节点 2 开始，第二个出发。在节点 0 处有一个洞。

在每个玩家的行动中，他们 必须 沿着图中与所在当前位置连通的一条边移动。例如，如果老鼠在节点 1 ，那么它必须移动到 graph[1] 中的任一节点。

此外，猫无法移动到洞中（节点 0）。

然后，游戏在出现以下三种情形之一时结束：

如果猫和老鼠出现在同一个节点，猫获胜。
如果老鼠到达洞中，老鼠获胜。
如果某一位置重复出现（即，玩家的位置和移动顺序都与上一次行动相同），游戏平局。
给你一张图 graph ，并假设两位玩家都都以最佳状态参与游戏：

如果老鼠获胜，则返回 1；
如果猫获胜，则返回 2；
如果平局，则返回 0 。
 
示例 1：


输入：graph = [[2,5],[3],[0,4,5],[1,4,5],[2,3],[0,2,3]]
输出：0
示例 2：


输入：graph = [[1,3],[0],[3],[0,2]]
输出：1
 

提示：

3 <= graph.length <= 50
1 <= graph[i].length < graph.length
0 <= graph[i][j] < graph.length
graph[i][j] != i
graph[i] 互不相同
猫和老鼠在游戏中总是可以移动
'''

class Solution:
    def catMouseGame(self, graph: List[List[int]]) -> int:
        n = len(graph)
        # color[m][c][t]：状态 (m, c, t) 的结果
        # 0：未知/和局，1：老鼠必胜，2：猫必胜
        color = [[[0, 0] for _ in range(n)] for _ in range(n)]
        # degree[m][c][t]：状态 (m, c, t) 出边的数量（还未确定结果的走法数）
        degree = [[[0, 0] for _ in range(n)] for _ in range(n)]
        
        # 初始化每个状态的度数
        for m in range(n):
            for c in range(n):
                degree[m][c][0] = len(graph[m])  # 老鼠回合：所有相邻节点均可选
                # 猫回合：猫不能走到洞口 0！
                degree[m][c][1] = sum(1 for x in graph[c] if x != 0)
        
        q = deque()
        
        # 终止状态1：老鼠在洞口，老鼠获胜
        for c in range(n):
            for t in range(2):
                if color[0][c][t] == 0:
                    color[0][c][t] = 1
                    q.append((0, c, t, 1))
        
        # 终止状态2：猫抓到老鼠（m==c，且 m!=0）
        for m in range(1, n):
            for t in range(2):
                if color[m][m][t] == 0:
                    color[m][m][t] = 2
                    q.append((m, m, t, 2))
        
        # 辅助函数：返回状态 (m, c, t) 的所有父状态
        def get_parents(m: int, c: int, t: int):
            parents = []
            if t == 0:
                # 当前状态是老鼠回合，说明上一步是猫走的，父状态形如 (m, c0, 1)
                # 要求：c 是 c0 的一个合法走法，并且猫不能从 0 出发，所以 c0 != 0
                for c0 in range(n):
                    if c0 == 0:
                        continue
                    if c in graph[c0]:
                        parents.append((m, c0, 1))
            else:
                # 当前状态是猫回合，说明上一步是老鼠走的，父状态形如 (m0, c, 0)
                # 要求：m 是 m0 的一个合法走法
                for m0 in range(n):
                    if m in graph[m0]:
                        parents.append((m0, c, 0))
            return parents
        
        # 反向递推：从终止状态向父状态更新结果
        while q:
            m, c, t, res = q.popleft()
            for m0, c0, t0 in get_parents(m, c, t):
                if color[m0][c0][t0] != 0:
                    continue
                # 如果父状态的操作者可以直接走到一个对自己有利的状态，则父状态结果确定
                if t0 == 0 and res == 1:  # 父状态老鼠回合，且当前状态老鼠必胜
                    color[m0][c0][t0] = 1
                    q.append((m0, c0, t0, 1))
                elif t0 == 1 and res == 2:  # 父状态猫回合，且当前状态猫必胜
                    color[m0][c0][t0] = 2
                    q.append((m0, c0, t0, 2))
                else:
                    # 否则，父状态的度数减 1（意味着有一种走法不能带来有利结果）
                    degree[m0][c0][t0] -= 1
                    # 当父状态没有任何走法能避免对手必胜时，父状态结果确定为对手获胜
                    if degree[m0][c0][t0] == 0:
                        if t0 == 0:
                            color[m0][c0][t0] = 2  # 老鼠回合，没有赢法，则猫必胜
                            q.append((m0, c0, t0, 2))
                        else:
                            color[m0][c0][t0] = 1  # 猫回合，没有赢法，则老鼠必胜
                            q.append((m0, c0, t0, 1))
        
        return color[1][2][0]
