#include<vector>
#include<algorithm>

#include "CvGameCoreDLL.h"
#include "CvGameCoreUtils.h"
#include "CvPlot.h"
#include "CvPlayer.h"

#define lc ch[x][0]
#define rc ch[x][1]
#define rep(i, l, r) for (int i = (l); i <= (r); i++)
typedef long long ll;
const int iWorldX = 150;
const int iWorldY = 80;
const int N = iWorldX * iWorldY + 1;

class CvLCT {
protected:
	int sz[N], f[N], ch[N][2], rev[N], si[N];

public:
	CvLCT() {
		for (int i = 0; i < N; i++)
		{
			sz[i] = 1;
			f[i] = 0;
			rev[i] = 0;
			si[i] = 0;

			ch[i][0] = 0;
			ch[i][1] = 0;
		}
		sz[0] = 0;
	}
	~CvLCT() {}

protected:
	// x 是否为根？
	bool isrt(int x) { return (!f[x]) || (ch[f[x]][0] != x && ch[f[x]][1] != x); }

	// !!更新 x 节点的值
	void upd(int x) { sz[x] = sz[lc] + sz[rc] + si[x] + 1; }

	// pushdown 操作
	void put(int x) { rev[x] ^= 1; }
	void pd(int x) {
		if (rev[x]) {
			put(lc), put(rc), put(x);
			std::swap(lc, rc);
		}
	}

	// 旋转操作
	void rot(int x) {
		int y = f[x], z = f[y], w = ch[y][1] == x;

		if (!isrt(y)) {
			ch[z][ch[z][1] == y] = x;
		}

		f[x] = z;
		f[y] = x;
		f[ch[x][w ^ 1]] = y;

		ch[y][w] = ch[x][w ^ 1];
		ch[x][w ^ 1] = y;

		upd(y);
	}
	void splay(int x) {

		std::vector<int> top;
		for (int i = x; !isrt(i); i = f[i]) {
			top.push_back(f[i]);
		}
		for (int i = top.size() - 1; i >= 0; i--){
			pd(top[i]);
		}
		top.clear();

		while (!isrt(x)) {
			int y = f[x], z = f[y];
			if (!isrt(y)) (ch[y][1] == x) ^ (ch[z][1] == y) ? rot(x) : rot(y);
			rot(x);
		}
		upd(x);
	}

	// 打通 x 到树根的链路
	void access(int x) {
		for (int y = 0; x; y = x, x = f[x]) {
			splay(x);
			// !!更新子树数据
			si[x] = si[x] + sz[rc] - sz[y];
			rc = y;
			upd(x);
		}
	}

	// 将 x 节点作为根
	void mkrt(int x) { access(x); splay(x); put(x); }

	// 求x节点的根
	int fdrt(int x) { 
		access(x); splay(x);  
		while (ch[x][0]) {
			x = ch[x][0];
		}
		return x;
	}

	// x 的父亲为y
	void link(int x, int y) {
		mkrt(x); access(y); splay(y);
		f[x] = y;
		// !!更新子树操作
		si[y] += sz[x];
		upd(y);
	}

	// 断开 x，y 的链接
	void cut(int x, int y) {
		mkrt(x); access(y); splay(y);
		if (ch[y][0] != x || ch[x][1]) return;
		f[ch[y][0]] = ch[y][0] = 0; upd(y);
	}

	// 查询 x 到 y 的数据
	ll que(int x, int y) { mkrt(x); access(y); splay(y); return 1ll * (sz[y] - sz[x]) * sz[x]; }

	int getPlotIndex(const CvPlot* pPlot) const { return pPlot->getX() + pPlot->getY() * iWorldX + 1; }
public:

	// y 加入到 x
	void Link(CvPlot* pPlotX, CvPlot* pPlotY)
	{
		int iX = getPlotIndex(pPlotX), iY = getPlotIndex(pPlotY);
		if (fdrt(iX) != fdrt(iY)) link(iX, iY);
	}

	// 移除 pPlot
	void Cut(CvPlot* pPlot, TeamTypes eTeam)
	{
		std::vector<CvPlot*> lPlotNeedUpdate;

		int iX, iY = getPlotIndex(pPlot);
		for (int i = 0; i < NUM_DIRECTION_TYPES; i++) 
		{
			CvPlot * pAdjacentPlot = plotDirection(pPlot->getX(), pPlot->getY(), DirectionTypes(i));

			if (pAdjacentPlot != NULL) {
				iX = getPlotIndex(pAdjacentPlot);
				if (fdrt(iX) == fdrt(iY))
				{
					cut(iX, iY);
					lPlotNeedUpdate.push_back(pAdjacentPlot);
				}
			}
		}

		for (size_t i = 0; i < lPlotNeedUpdate.size() - 1; i++) 
		{
			for (size_t j = i; j < lPlotNeedUpdate.size(); j++)
			{
				CvPlot* pNeedUpdateX = lPlotNeedUpdate[i];
				CvPlot* pNeedUpdateY = lPlotNeedUpdate[j];
				if (pNeedUpdateX->isTradeNetwork(eTeam) && pNeedUpdateY->isTradeNetwork(eTeam))
				{
					if (pNeedUpdateX->isTradeNetworkConnected(pNeedUpdateY, eTeam))
					{
						Link(pNeedUpdateX, pNeedUpdateY);
					}
				}
			}
		}
	}

	int GetLength(CvPlot* pPlot)
	{
		int root = fdrt(getPlotIndex(pPlot));
		return sz[root];
	}
};

#undef lc
#undef rc