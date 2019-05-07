from sqlalchemy import func
from app import app, db
from flask import render_template, url_for, redirect, flash, request, send_from_directory
from app.forms import LoginForm, PublishForm, UseraddForm, SetpwdForm, UpgradeFrom
from flask_login import login_required, current_user, logout_user, login_user
from app.models import User, Package, UpgradeLog
import os, time


@app.route('/')
@app.route('/index')
@login_required
def index():
    # user = {'username': 'jokerzhang'}
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('用户名或密码错误')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/setPwd', methods=['GET', 'POST'])
@login_required
def setPwd():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = SetpwdForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        print(user)
        print(user.check_password(form.old_passwd.data))
        print(form.new_passwd.data)
        print(form.new_passwd2.data)
        if user.check_password(form.old_passwd.data):
            if form.new_passwd.data == form.new_passwd2.data:
                user.set_password(form.new_passwd2.data)
                db.session.commit()
                flash('密码修改成功，请重新登录')
                print('123')
                logout_user()
                return redirect(url_for('login'))
            else:
                print('234')
                flash('两次新密码不一致，请重新输入')
                return redirect(url_for('setPwd'))
        else:
            flash('旧密码输入错误，请重新输入')
            return redirect(url_for('setPwd'))
    return render_template('setPwd.html', form=form)


@app.route('/upgrade', methods=['GET', 'POST'])
def upgrade():
    page = request.args.get('page', 1, type=int)
    upgrade_data = UpgradeLog.query.order_by(UpgradeLog.create_time.desc()).paginate(
        page, app.config['UPGRADE_PER_PAGE'], False)
    next_url = url_for('upgrade', page=upgrade_data.next_num) \
        if upgrade_data.has_next else None
    prev_url = url_for('upgrade', page=upgrade_data.prev_num) \
        if upgrade_data.has_prev else None
    return render_template('upgrade_list.html', upgrade_data=upgrade_data.items,
                           next_url=next_url, prev_url=prev_url)


@app.route('/upgrade_add', methods=['GET', 'POST'])
def upgrade_add():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = UpgradeFrom()
    if form.validate_on_submit():
        upgrade_info = UpgradeLog(title=form.title.data,
                                  content=form.content.data,
                                  creator=current_user.username,
                                  create_time=time.strftime('%Y-%m-%d %H:%M:%S'))
        try:
            db.session.add(upgrade_info)
            db.session.commit()
            return redirect(url_for('upgrade'))
        except Exception as e:
            db.session.rollback()
            raise e
    return render_template('upgrade.html', form=form)


@app.route('/upgrade_edit/<id>', methods=['GET', 'POST'])
def upgrade_edit(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = UpgradeFrom()
    upgrade_info = UpgradeLog.query.filter_by(id=id).first()
    if form.validate_on_submit():
        upgrade_info.title = form.title.data
        upgrade_info.content = form.content.data
        upgrade_info.creator = current_user.username
        upgrade_info.modify_time = time.strftime('%Y-%m-%d %H:%M:%S')
        try:
            db.session.commit()
            return redirect(url_for('upgrade_details', id=id))
        except Exception as e:
            db.session.rollback()
            raise e
    elif request.method == 'GET':
        form.title.data = upgrade_info.title
        form.content.data = upgrade_info.content
    return render_template('upgrade.html', form=form)


@app.route('/upgrade_details/<id>', methods=['GET'])
def upgrade_details(id):

    upgrade_detail = UpgradeLog.query.filter_by(id=id).first()
    return render_template('upgrade_details.html', upgrade_detail=upgrade_detail)


@app.route('/package')
def package():
    packages = Package.query.order_by(Package.create_time.desc())
    print(packages)
    return render_template('package.html', packages=packages)


@app.route('/submit_package', methods=['GET', 'POST'])
def submit_package():
    form = PublishForm()
    id = db.session.query(func.max(Package.id)).first()
    print(id, current_user.is_authenticated)
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if request.method == 'POST':
        print(1)
        print(form.validate_on_submit())
        flash(form.errors)
        #print(form.package_version.data)
        if form.validate_on_submit():
            print(2)
            #print(request.files['pack'])
            file = request.files['package']
            file_path = 'packages/{}'.format(file.filename)
            print(file_path)
            file.save('app/packages/{}'.format(file.filename))
            package_info = Package(package_name=file.filename,
                                   package_content=form.package_content.data,
                                   author=current_user,
                                   package_path=file_path,
                                   package_version=form.package_version.data)
            db.session.add(package_info)
            db.session.commit()
            print(os.path.abspath('app/packages/license'))
            if os.path.exists(file_path):
                print('upload1')
                flash('Upgrade package submit success.')
            else:
                print('upload2')
            return redirect(url_for('package'))
    if request.method == 'GET':
        form.package_id.data = id[0] + 1
    return render_template('submit_package.html',
                           title=u'提交更新', form=form)


@app.route('/packages/<filename>')
def download_package(filename):
    return send_from_directory('packages', filename, as_attachment=True)


@app.route('/user')
def user():
    users = User.query.all()
    print(users)
    return render_template('user.html', users=users)


@app.route('/useradd', methods=['GET', 'POST'])
def useradd():
    form = UseraddForm()
    if form.validate_on_submit():
        if not User.query.filter_by(username=form.user_name.data).first():
            user = User(username=form.user_name.data, email=form.user_email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user'))
        else:
            flash('用户已存在')
            return render_template('useradd.html', form=form)
    return render_template('useradd.html', form=form)
