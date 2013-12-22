#!/usr/bin/env python
#coding=utf-8

"""
    forms: blog.py
    ~~~~~~~~~~~~~

    :license: BSD, see LICENSE for more details.
"""
from flask.ext.wtf import Form
from wtforms import TextAreaField, SubmitField, TextField, ValidationError
from wtforms.validators import DataRequired, Email, URL, Optional
from flask.ext.babel import gettext, lazy_gettext as _ 

from pypress.helpers import slugify
from pypress.extensions import db
from pypress.models import Post


class PostForm(Form):

    title = TextField(_("Title"), validators=[
                      DataRequired(message=_("Title required"))])

    slug = TextField(_("Slug"))

    content = TextAreaField(_("Content"))

    tags = TextField(_("Tags"), validators=[
                      DataRequired(message=_("Tags required"))])

    submit = SubmitField(_("Save"))

    def __init__(self, *args, **kwargs):
        self.post = kwargs.get('obj', None)
        super(PostForm, self).__init__(*args, **kwargs)

    def validate_slug(self, field):
        if len(field.data) > 50:
            raise ValidationError, gettext("Slug must be less than 50 characters")
        slug = slugify(field.data) if field.data else slugify(self.title.data)[:50]
        posts = Post.query.filter_by(slug=slug)
        if self.post:
            posts = posts.filter(db.not_(Post.id==self.post.id))
        if posts.count():
            error = gettext("This slug is taken") if field.data else gettext("Slug is required")
            raise ValidationError, error


class CommentForm(Form):

    email = TextField(_("Email"), validators=[
                      DataRequired(message=_("Email required")),
                      Email(message=_("A valid email address is required"))])
    
    nickname = TextField(_("Nickname"), validators=[
                      DataRequired(message=_("Nickname required"))])
    
    website = TextField(_("Website"), validators=[
                    Optional(),
                    URL(message=_("A valid url is required"))])
    
    comment = TextAreaField(_("Comment"), validators=[
                      DataRequired(message=_("Comment required"))])
    
    submit = SubmitField(_("Add comment"))
    cancel = SubmitField(_("Cancel"))


class LinkForm(Form):

    name = TextField(_("Site name"), validators=[
                      DataRequired(message=_("Name required"))])
    
    link = TextField(_("link"), validators=[
                    URL(message=_("A valid url is required"))])
    
    email = TextField(_("Email"), validators=[
                    Email(message=_("A valid email is required"))])
    
    logo = TextField(_("Logo"), validators=[
                    Optional(),
                    URL(message=_("A valid url is required"))])
    
    description = TextAreaField(_("Description"))

    submit = SubmitField(_("Save"))


class TemplateForm(Form):

    html = TextAreaField(_("HTML"), validators=[
                    DataRequired(message=_("HTML required"))])
    
    submit = SubmitField(_("Save"))
    cancel = SubmitField(_("Cancel"))

