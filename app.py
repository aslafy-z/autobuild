#!/usr/bin/env python3

import logging
from os import environ

from asyncio import sleep
from aiohttp import web
from google.cloud.devtools import cloudbuild_v1

logging.basicConfig(level=logging.DEBUG)

GOOGLE_PROJECT_ID = 'autobuild'

UPSTREAM_PREFIX = environ.get('UPSTREAM_PREFIX', GOOGLE_PROJECT_ID)
UPSTREAM_REGISTRY = environ.get('UPSTREAM_REGISTRY', 'gcr.io')
UPSTREAM_REGISTRY_URL = environ.get('UPSTREAM_REGISTRY_URL', 'https://{}'.format(UPSTREAM_REGISTRY))
UPSTREAM_REPO = environ.get('UPSTREAM_REPO', '{}/{}'.format(UPSTREAM_REGISTRY, UPSTREAM_PREFIX))

client = cloudbuild_v1.CloudBuildClient()

app = web.Application()
routes = web.RouteTableDef()


def build_start(owner, repo, ref):
    image = f'{UPSTREAM_REPO}/{owner}/{repo}:{ref}'
    return client.create_build(GOOGLE_PROJECT_ID, dict(
        images=[image],
        steps=[
            dict(name='gcr.io/cloud-builders/git', args=['clone', f'https://github.com/{owner}/{repo}', '.']),
            dict(name='gcr.io/cloud-builders/git', args=['checkout', ref]),
            dict(name='gcr.io/cloud-builders/docker', args=['build', '-t', image, '.']),
        ],
    ))


def build_is_running(image):
    return len(list(client.list_builds(GOOGLE_PROJECT_ID, filter_=f'results.images.name="{image}" AND (status="WORKING" OR status="QUEUED")'))) > 0


def build_is_ready(image):
    return len(list(client.list_builds(GOOGLE_PROJECT_ID, filter_=f'results.images.name="{image}" AND status="SUCCESS"'))) > 0


def check_build(owner, repo, ref):
    image_url = f'{UPSTREAM_REPO}/{owner}/{repo}:{ref}'
    if build_is_ready(image_url):
        return True
    if build_is_running(image_url):
        return False
    build_start(owner, repo, ref)
    return False


def send_to_upstream(to):
    raise web.HTTPFound(f'{UPSTREAM_REGISTRY_URL}{to}')


def send_for_a_trip(to, step=10, count=5):
    raise web.HTTPFound(f'/_trip?to={to}&step={step}&count={count}')


@routes.get('/v2/' + UPSTREAM_PREFIX + '/{owner}/{repo}/{verb}/{ref}')
async def manifest_handler(request):
    owner = request.match_info['owner']
    repo = request.match_info['repo']
    ref = request.match_info['ref']
    # FIXME: SHA references are not supported as we cannot detect if image or layer
    if 'sha256:' in ref:
        return send_to_upstream(request.url.path)
    ready = await check_build(owner, repo, ref)
    if ready:
        return send_to_upstream(request.url.path)
    return send_for_a_trip(request.url.path)


@routes.get('/v2/{tail:.*}')
async def catchall_handler(request):
    return send_to_upstream(request.url.path)


@routes.get('/_trip')
async def trip_handler(request):
    step = int(request.query['step'])
    count = int(request.query['count'])
    to = request.query['to']
    await sleep(step)
    if count == 1:
        raise web.HTTPFound(to)
    return send_for_a_trip(to=to, step=step, count=count - 1)


app.add_routes(routes)
web.run_app(app, host='localhost', port=8888)
