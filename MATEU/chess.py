import os, sys
from threading import Thread
try: 
    import chess
except ModuleNotFoundError: 
    os.system("pip install chess")
    import chess
import chess.svg

def thrStart(number_of_threads,func_list,arguments=None,daemon=0):
    newThreads=[]
    results=[None]*number_of_threads
    if len(func_list)==1:
        func_list*=number_of_threads
    if arguments==None:
        for i in range(number_of_threads-1):
            newThreads.append(Thread(target = func_list[i],args=(results,i),daemon=daemon))
            newThreads[i].start()
    else:
        for i in range(number_of_threads-1):
            newThreads.append(Thread(target = func_list[i], args=(results,i)+arguments[i], daemon=daemon))
            newThreads[i].start()
    return (newThreads, results)
def thrJoin(newThreads,results):
    for i in newThreads:
        i.join()
    return results


    
class Chess:
        def __init__(self,constants=None, empty_square="·"):
            self.piece={
                0:empty_square,
                -2000:"k", #black king
                -90:"q", #black queen
                -50:"r", #black king rook
                -49:"r", #black queen rook
                -32:"b", #black bishop
                -29:"n", #black knight
                -10:"p", #black 
                10:"P", #white 
                29:"N", #white knight
                32:"B", #white bishop
                49:"R", #white rook
                50:"R", #white rook
                90:"Q", #white queen
                2000:"K", #white king
                "k":-2000, #black king
                "q":-90, #black queen
                "r":-49, #black queen's rook
                "b":-32, #black bishop
                "n":-29, #black knight
                "p":-10, #black 
                "P":10, #white 
                "N":29, #white knight
                "B":32, #white bishop
                "R":49, #white queen's rook
                "Q":90, #white queen
                "K":2000, #white king
            }
            
            if constants==None:
                self.Board,self.turn,self.kingsmoved,self.rooksmoved,self.enpassant,self.push_or_take,self.movecount,self.fenregister=[[-49,-29,-32,-90,-2000,-32,-29,-50],[-10,-10,-10,-10,-10,-10,-10,-10],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[10,10,10,10,10,10,10,10],[49,29,32,90,2000,32,29,50]],1,[0,0],[0,0,0,0],"",0,1,[]
            else:
                (self.Board, self.turn, self.kingsmoved, self.rooksmoved, self.enpassant, self.push_or_take, self.movecount, self.fenregister)=constants
            self.get_fen()
        def UCI_to_NCN(self,uci,a={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}): 
            if len(uci)==4:
                return ((8-int(uci[1]),a[uci[0]]),(8-int(uci[3]),a[uci[2]]),"")
            else:
                return ((8-int(uci[1]),a[uci[0]]),(8-int(uci[3]),a[uci[2]]), (self.piece[uci[4].upper()] if self.turn else self.piece[uci[4]]))
        def push(self,uci=None):
            self.fenregister.append(self.fen)
            if uci==None:
                c=self.legalMoves()
                uci=str(input("Enter UCI move: "))
                while not uci in c:
                    uci=str(input("Enter UCI move: "))
            move=self.UCI_to_NCN(uci)
            piece=self.Board[move[0][0]][move[0][1]]
            b=self.Board[move[1][0]][move[1][1]]
            if piece==10 and move[0][0]==6 and move[1][0]==4:
                self.enpassant=uci[0]+"3"
            elif piece==-10 and move[0][0]==1 and move[1][0]==3:
                self.enpassant=uci[0]+"6"
            else:
                self.enpassant=""
            if piece in {10,-10} or b:
                self.push_or_take=0
            else:
                self.push_or_take+=1
            if piece==2000:
                self.kingsmoved[0]=1
            elif piece==-2000:
                self.kingsmoved[1]=1
            elif move[0]==[7,7]:
                self.rooksmoved[0]=1
            elif move[0]==[7,0]:
                self.rooksmoved[1]=1
            elif move[0]==[0,7]:
                self.rooksmoved[2]=1
            elif move[0]==[0,0]:
                self.rooksmoved[3]=1
            if move[2]!="":
                piece=move[2]
            self.Board[move[0][0]][move[0][1]]=0
            self.Board[move[1][0]][move[1][1]]=piece
            self.turn=not self.turn
            self.movecount+=self.turn
            self.get_fen()
            return uci
        def show(self,mode=None):
            if mode in {None,"None",0}:
                os.system("clear" if os.name=="posix" else "cls")
                sys.stdout.write("\n".join([" ".join([self.piece[j] for j in i]) for i in self.Board])+"\n")   
            elif mode==1:
                os.system("clear" if os.name=="posix" else "cls")
                sys.stdout.write("  ╔"+"═══╦"*8+"\b╗\n"+(" ║\n- ╠"+"═══╬"*8+"\b╣\n").join(f"{8-jj} "+" ".join(["║ "+self.piece[j] for j in self.Board[jj]]) for jj in (0,1,2,3,4,5,6,7))+f" ║\n  ╚"+"═══╩"*8+"\b╝\n"+"   ".join(" abcdefgh\n"))         
            else:
                print(str(chess.svg.board(chess.Board(self.fen), size=350)),file=open("board.svg", "w"))
        def get_fen(self):
            fen=""
            n=8
            for i in self.Board:
                k=0
                b=0
                for j in i:
                    if b and j==0:
                        k+=1
                    elif b:
                        fen+=str(k)+self.piece[j] 
                        k=0
                        b=0
                    elif j==0:
                        k=1
                        b=1
                    else:
                        fen+=self.piece[j] 
                if b:
                    fen+=str(k)
                n-=1
                if n>0:
                    fen+="/"
            if self.turn:
                fen+=" w "
            else:
                fen+=" b "
            if self.kingsmoved[0] or (self.rooksmoved[0] and self.rooksmoved[1]):
                wk=""
            elif self.rooksmoved[0]:
                wk="K"
            elif self.rooksmoved[1]:
                wk="Q"
            else:
                wk="KQ"
            if self.kingsmoved[1] or (self.rooksmoved[2] and self.rooksmoved[3]):
                bk=""
            elif self.rooksmoved[2]:
                bk="k"
            elif self.rooksmoved[3]:
                bk="q"
            else:
                bk="kq"
            kk=wk+bk+" "
            if kk==" ":
                if self.enpassant=="":
                    fen+=f"- - {self.push_or_take} {self.movecount}"
                else:
                    fen+=f"- {self.enpassant} {self.push_or_take}   {self.movecount}"
            else:
                if self.enpassant=="":
                    fen+=f"{kk}- {self.push_or_take} {self.movecount}"
                else:
                    fen+=f"{kk}{self.enpassant} {self.push_or_take}   {self.movecount}"
            self.fen=str(fen)
        def legalMoves(self):
            a=chess.Board(self.fen).generate_legal_moves()
            return set(map(str,a))
        def gamestatus(self):
            a=chess.Board(self.fen)
            if a.is_checkmate():
                return (1,not self.turn)
            elif self.push_or_take>=50 or a.is_stalemate() or a.is_insufficient_material():
                return (1,None)
            del a
            b=self.halfen(self.fen)
            if sum(b in i for i in self.fenregister)>2: return (1,None)
            return (0,None)
        def halfen(self, fen):
            half=""
            for i in fen:
                if i==" ":
                    return half
                else:
                    half+=i
        def after_move_score(self):
            a=self.gamestatus()
            if a[0]:
                if a[1]==None:
                    return -20*(-1**self.turn)
                return -4000*(-1**self.turn)
            else:
                return sum(tuple(map(sum,self.Board)))
        def before_move_score(self):
            a=self.gamestatus()
            if a[0]:
                if a[1]==None:
                    return 20*(-1**self.turn)
                return 4000*(-1**self.turn)
            else:
                return sum(tuple(map(sum,self.Board)))
        def undo(self):
            a=self.fenregister
            del self
            k=len(a)-1
            b=a[k]
            del a[k]
            constants=fromfen(b,a)
            new_Board=Chess(constants)
            return new_Board

def fromfen(fe,fenreg=None):
    d={"k":-2000,"q":-90,"r":-49,"b":-32,"n":-29,"p":-10,"P":10,"N":29,"B":32,"R":49,"Q":90,"K":2000}
    fenregister=[]
    if fenreg!=None:
        for i in fenreg:
            fenregister.append(str(i))
    a=1
    b=0
    Board=[]
    kingsmoved=[1,1]
    rooksmoved=[1,1,1,1]
    c=[]
    for i in fe:
        if b==0:
            if a:
                if i=="/":
                    Board.append(c)
                    c=[]
                elif i in {"1","2","3","4","5","6","7","8"}:
                    c+=[0,]*int(i)
                elif i==" ":
                    Board.append(c)
                    a=0
                else:
                    c.append(d[i])
            else:
                if i=="w":
                    turn=1
                elif i=="b":
                    turn=0
                elif i==" ":
                    b=1
        elif b==1:
            if i=="K":
                kingsmoved[0]=0
                rooksmoved[0]=0
            elif i=="Q":
                kingsmoved[0]=0
                rooksmoved[1]=0
            elif i=="k":
                kingsmoved[1]=0
                rooksmoved[2]=0
            elif i=="k":
                kingsmoved[1]=0
                rooksmoved[3]=0
            elif i==" ":
                b=2
        elif b==2:
            if i=="-":
                enpassant=""
            elif i==" ":
                b=3
            elif a:
                enpassant+=i
            else:
                enpassant=i
                a=1
        elif b==3:
            if i!=" ":
                push_or_take=int(i)
            else:
                b=4
        else:
            if i!=" ":
                movecount=int(i)
    return (Board,turn,kingsmoved,rooksmoved,enpassant,push_or_take,movecount,fenregister)
class engine:
    def __init__(self, board=None, depth=0): 
        if board==None:
            board=Chess()
        self.board,self.depth,self.DEPTH=board,depth,depth
    def get(self, move=None): 
        a=(self.board.after_move_score(),move) if self.depth==0 or self.board.gamestatus()[0] else (max(map(self.get_score,self.board.legalMoves())) if self.board.turn else min(map(self.get_score,self.board.legalMoves())))
        return tuple(a)
    def get_score(self, move):
        self.board.push(move)
        self.depth-=1
        a=self.get(move)[0]*1000+self.board.after_move_score() if self.depth==self.DEPTH else self.get(move)[0]
        self.depth+=1
        self.board=self.board.undo()
        return (a,move)