import tkinter as tk
import chart_writer_bar
import chart_publisher_bar
import chart_disp_pi

def close_win(root_chart):
    root_chart.quit()
    root_chart.destroy()
def veiw_chart():
    chart_writer_bar.writer_chart()   
    chart_publisher_bar.publisher_chart()  
    chart_disp_pi.union_chart()
    # 独立したウィンドウでないと上手くいかない
    root_chart = tk.Tk()
    # WM_DELETE_WINDOWウィンドウが閉じられるに発生するイベント
    # 引数付き関数はlambda式
    root_chart.protocol("WM_DELETE_WINDOW", lambda :close_win(root_chart))
    root_chart.geometry("450x900+700+30")
    root_chart.title("グラフ:著者/出版社/廃棄率" )
    canvas_w = tk.Canvas(root_chart, bg="orange", height=300, width=450) 
    canvas_w.place(x=0, y=0)
    canvas_p = tk.Canvas(root_chart, bg="orange", height=300, width=450) 
    canvas_p.place(x=0, y=300)
    canvas_u = tk.Canvas(root_chart, bg="orange", height=300, width=450) 
    canvas_u.place(x=0, y=600)

    img_w = tk.PhotoImage(master=root_chart, file="image/writer_bar_chart.png", width=450, height=300)
    img_p = tk.PhotoImage(master=root_chart, file="image/publisher_bar_chart.png", width=450, height=300)
    img_u = tk.PhotoImage(master=root_chart, file="image/chart_disp_pi.png", width=450, height=300)
    canvas_w.create_image(0, 0, image=img_w, anchor=tk.NW)
    canvas_p.create_image(0, 0, image=img_p, anchor=tk.NW)
    canvas_u.create_image(0, 0, image=img_u, anchor=tk.NW)
    root_chart.mainloop()
    

if __name__ == '__main__':
    veiw_chart()
