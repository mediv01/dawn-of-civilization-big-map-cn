#pragma once

// plotGroup.h

#ifndef CIV4_PLOT_GROUP_H
#define CIV4_PLOT_GROUP_H

//#include "CvStructs.h"
#include "LinkedList.h"
#include <set>
using std::set;

class CvPlot;
/*
	1. addPlot 增加点 - 连边
	2. removePlot 删除点 - 删边
	3. getNumBonuses 查询资源(eBonus)数量 - 子树求和
	4. operator== 判断两点连通性 - 求根
	5. changeNumBonuses 修改资源(eBonus)数量 - 修改节点权值
	6. getLengthPlots - 求子树大小
*/
class CvPlotGroup
{

public:

	CvPlotGroup();
	virtual ~CvPlotGroup();

	void init(int iID, PlayerTypes eOwner, CvPlot* pPlot);
	void uninit();
	void reset(int iID = 0, PlayerTypes eOwner = NO_PLAYER, bool bConstructorCall=false);

	void addPlot(CvPlot* pPlot);
	//void addPlot(CvPlot* pPlotX, CvPlot* pPlotY); // wunshare - 连边
	void removePlot(CvPlot* pPlot);
	//void removePlot(CvPlot* pPlotX, CvPlot* pPlotY); // wunshare - 删边
	//bool operator==(const CvPlotGroup* p1, const CvPlotGroup* p2) const; // wunshare
	void recalculatePlots();

	void printPlotGroups();

	int getNumCities() const;

	int getID() const;
	void setID(int iID);

	PlayerTypes getOwner() const;
#ifdef _USRDLL
	inline PlayerTypes getOwnerINLINE() const
	{
		return m_eOwner;
	}
#endif
	int getNumBonuses(BonusTypes eBonus) const;
	bool hasBonus(BonusTypes eBonus);										
	void changeNumBonuses(BonusTypes eBonus, int iChange);

	void insert(XYCoords xy);

	void combine(CvPlotGroup* plotgroup);

	CvPlot* begin();
	CvPlot* next();
	CvPlot* erase(CvPlot* pPlot);

	int getLengthPlots();

	// for serialization
	void read(FDataStreamBase* pStream);
	void write(FDataStreamBase* pStream);

protected:

	int m_iID;

	PlayerTypes m_eOwner;

	int* m_paiNumBonuses;

	CLinkList<XYCoords> m_plots;

	set<XYCoords> m_splot;
	set<XYCoords>::iterator itor;

	set<CvCity*> m_sCities;
};

/*
class LCTree {
public:
	LCTree() {
		const int MAXN = GC.getMapINLINE().getGridWidth() * GC.getMapINLINE().getGridHeight() + 1;
		lc = new int[MAXN];
		rc = new int[MAXN];
		fa = new int[MAXN];
		rev = new int[MAXN];
	}
	~LCTree() {
		delete []c;
		delete []fa;
		delete []rev;
	}

	void access(int x) { // 连接一条x到根的重链
		for (int y = 0; x; y=x, x = fa[x]) {
			splay(x);
			//si[x] = si[x] + sz[rc[x]] - sz[y];
			rc[x] = y;
			update(x);
		}
	}

	int findroot(int x) { // 查找x的根节点
		access(x);
		splay(x);
		while(lc[x]) {
			x = lc[x];
		}
		return x;
	}

	void link(int x, int y) { // 连一条x到y的虚边
		makeroot(x);
		access(y);
		splay(y);
		fa[x] = y;
		//si[y] += sz[x];
		update(y);
	}

private:
	void makeroot(int x) {
		access(x);
		splay(x);
		put(x);
	}
	void put(x) {
		swap(lc[x], rc[x]);
		rev[x] ^= 1;
	}
private:
	int* lc;
	int* rc;
	int* fa;
	int* rev;
	// int** m_paiNumBonuses;
};
*/

#endif
