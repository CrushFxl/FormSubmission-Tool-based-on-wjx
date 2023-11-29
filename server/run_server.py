from settings import create_app

app, db = create_app()

with app.app_context():
    with db.engine.connect() as conn:
        rs = conn.execute("select 1")
        print(rs.fetchone())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=12345)
