import React, { Component } from 'react';
import APIObject from '../Common/APIObject';
import PropTypes from 'prop-types';
import makePropertiesBox from '../Common/makePropertiesBox';
import ParameterItem from '../Common/ParameterItem';
import { makeControlPanel, makeControlButton } from '../Common/controlButton';
import { COLLECTIONS, IAM_POLICIES, USER_POST_ACTION, OPERATION_VIEW_SETTING, RESPONCE_STATUS } from '../../constants';
import { validatePassword } from '../Common/passwordUtils';
import {renderHubItem} from '../Graph/HubEntryListNode';
import SortableTree from "react-sortable-tree";
import { PluginsProvider } from '../../contexts';
import cookie from 'react-cookies';

import './style.css';
import './node-renderer-default.css';
import './placeholder-renderer-default.css';
import './react-sortable-tree.css';
import './tree-node.css';
import FileExplorerTheme from 'react-sortable-tree-theme-file-explorer';

const NODE_VIEW_MODES = [OPERATION_VIEW_SETTING.KIND_AND_TITLE, OPERATION_VIEW_SETTING.TITLE_AND_DESCRIPTION];


function findError(treeDataChildren) {
  console.log('findError', treeDataChildren);
  if (!treeDataChildren) {
      return false;
  }
  for (const treeData of treeDataChildren) {
      if (treeData.children && treeData.children.length > 0) {
        if (treeData.canExpand !== undefined && !treeData.canExpand) {
            return true;
        }
        if (findError(treeData.children)) {
            return true;
        }
      }
  }
  return false;
}

const PLUGINS_DICT = {"resources_dict": {"file": {"kind": "file", "title": "File", "cls": "plynx.plugins.resources.common.File", "icon": "feathericons.file", "color": "#fff"}, "pdf": {"kind": "pdf", "title": "PDF file", "cls": "plynx.plugins.resources.common.PDF", "icon": "plynx.pdf", "color": "#ffffff"}, "image": {"kind": "image", "title": "Image", "cls": "plynx.plugins.resources.common.Image", "icon": "plynx.image", "color": "#ffffff"}, "csv": {"kind": "csv", "title": "CSV file", "cls": "plynx.plugins.resources.common.CSV", "icon": "plynx.csv", "color": "#ffffff"}, "tsv": {"kind": "tsv", "title": "TSV file", "cls": "plynx.plugins.resources.common.TSV", "icon": "plynx.tsv", "color": "#ffffff"}, "json": {"kind": "json", "title": "JSON file", "cls": "plynx.plugins.resources.common.Json", "icon": "plynx.json", "color": "#ffffff"}, "executable": {"kind": "executable", "title": "Executable", "cls": "plynx.plugins.resources.common.Executable", "icon": "feathericons.play", "color": "#fcff57"}, "directory": {"kind": "directory", "title": "Directory", "cls": "plynx.plugins.resources.common.Directory", "icon": "feathericons.folder", "color": "#f44"}, "cloud-storage": {"kind": "cloud-storage", "title": "Cloud Storage", "cls": "plynx.plugins.resources.cloud_resources.CloudStorage", "icon": "feathericons.hard-drive", "color": "#5ed1ff"}}, "operations_dict": {"basic-file": {"kind": "basic-file", "title": "File", "executor": "plynx.plugins.executors.local.File", "hubs": [], "resources": [{"kind": "file", "title": "File", "cls": "plynx.plugins.resources.common.File", "icon": "feathericons.file", "color": "#fff"}, {"kind": "pdf", "title": "PDF file", "cls": "plynx.plugins.resources.common.PDF", "icon": "plynx.pdf", "color": "#ffffff"}, {"kind": "image", "title": "Image", "cls": "plynx.plugins.resources.common.Image", "icon": "plynx.image", "color": "#ffffff"}, {"kind": "csv", "title": "CSV file", "cls": "plynx.plugins.resources.common.CSV", "icon": "plynx.csv", "color": "#ffffff"}, {"kind": "tsv", "title": "TSV file", "cls": "plynx.plugins.resources.common.TSV", "icon": "plynx.tsv", "color": "#ffffff"}, {"kind": "json", "title": "JSON file", "cls": "plynx.plugins.resources.common.Json", "icon": "plynx.json", "color": "#ffffff"}, {"kind": "executable", "title": "Executable", "cls": "plynx.plugins.resources.common.Executable", "icon": "feathericons.play", "color": "#fcff57"}, {"kind": "directory", "title": "Directory", "cls": "plynx.plugins.resources.common.Directory", "icon": "feathericons.folder", "color": "#f44"}, {"kind": "cloud-storage", "title": "Cloud Storage", "cls": "plynx.plugins.resources.cloud_resources.CloudStorage", "icon": "feathericons.hard-drive", "color": "#5ed1ff"}], "icon": "feathericons.file", "color": "#fff", "is_static": true}, "basic-bash-jinja2-operation": {"kind": "basic-bash-jinja2-operation", "title": "BashJinja2 Operation", "executor": "plynx.plugins.executors.local.BashJinja2", "hubs": [], "resources": [{"kind": "file", "title": "File", "cls": "plynx.plugins.resources.common.File", "icon": "feathericons.file", "color": "#fff"}, {"kind": "pdf", "title": "PDF file", "cls": "plynx.plugins.resources.common.PDF", "icon": "plynx.pdf", "color": "#ffffff"}, {"kind": "image", "title": "Image", "cls": "plynx.plugins.resources.common.Image", "icon": "plynx.image", "color": "#ffffff"}, {"kind": "csv", "title": "CSV file", "cls": "plynx.plugins.resources.common.CSV", "icon": "plynx.csv", "color": "#ffffff"}, {"kind": "tsv", "title": "TSV file", "cls": "plynx.plugins.resources.common.TSV", "icon": "plynx.tsv", "color": "#ffffff"}, {"kind": "json", "title": "JSON file", "cls": "plynx.plugins.resources.common.Json", "icon": "plynx.json", "color": "#ffffff"}, {"kind": "executable", "title": "Executable", "cls": "plynx.plugins.resources.common.Executable", "icon": "feathericons.play", "color": "#fcff57"}, {"kind": "directory", "title": "Directory", "cls": "plynx.plugins.resources.common.Directory", "icon": "feathericons.folder", "color": "#f44"}, {"kind": "cloud-storage", "title": "Cloud Storage", "cls": "plynx.plugins.resources.cloud_resources.CloudStorage", "icon": "feathericons.hard-drive", "color": "#5ed1ff"}], "icon": "feathericons.terminal", "color": "#0f0", "is_static": false}, "basic-python-node-operation": {"kind": "basic-python-node-operation", "title": "Python Operation", "executor": "plynx.plugins.executors.local.PythonNode", "hubs": [], "resources": [{"kind": "file", "title": "File", "cls": "plynx.plugins.resources.common.File", "icon": "feathericons.file", "color": "#fff"}, {"kind": "pdf", "title": "PDF file", "cls": "plynx.plugins.resources.common.PDF", "icon": "plynx.pdf", "color": "#ffffff"}, {"kind": "image", "title": "Image", "cls": "plynx.plugins.resources.common.Image", "icon": "plynx.image", "color": "#ffffff"}, {"kind": "csv", "title": "CSV file", "cls": "plynx.plugins.resources.common.CSV", "icon": "plynx.csv", "color": "#ffffff"}, {"kind": "tsv", "title": "TSV file", "cls": "plynx.plugins.resources.common.TSV", "icon": "plynx.tsv", "color": "#ffffff"}, {"kind": "json", "title": "JSON file", "cls": "plynx.plugins.resources.common.Json", "icon": "plynx.json", "color": "#ffffff"}, {"kind": "executable", "title": "Executable", "cls": "plynx.plugins.resources.common.Executable", "icon": "feathericons.play", "color": "#fcff57"}, {"kind": "directory", "title": "Directory", "cls": "plynx.plugins.resources.common.Directory", "icon": "feathericons.folder", "color": "#f44"}, {"kind": "cloud-storage", "title": "Cloud Storage", "cls": "plynx.plugins.resources.cloud_resources.CloudStorage", "icon": "feathericons.hard-drive", "color": "#5ed1ff"}], "icon": "plynx.python-logo-notext", "color": "", "is_static": false}, "k8s-bash-jinja2-operation": {"kind": "k8s-bash-jinja2-operation", "title": "Kubernetes BashJinja2", "executor": "plynx.plugins.executors.kubernetes.BashJinja2", "hubs": [], "resources": [{"kind": "file", "title": "File", "cls": "plynx.plugins.resources.common.File", "icon": "feathericons.file", "color": "#fff"}, {"kind": "pdf", "title": "PDF file", "cls": "plynx.plugins.resources.common.PDF", "icon": "plynx.pdf", "color": "#ffffff"}, {"kind": "image", "title": "Image", "cls": "plynx.plugins.resources.common.Image", "icon": "plynx.image", "color": "#ffffff"}, {"kind": "csv", "title": "CSV file", "cls": "plynx.plugins.resources.common.CSV", "icon": "plynx.csv", "color": "#ffffff"}, {"kind": "tsv", "title": "TSV file", "cls": "plynx.plugins.resources.common.TSV", "icon": "plynx.tsv", "color": "#ffffff"}, {"kind": "json", "title": "JSON file", "cls": "plynx.plugins.resources.common.Json", "icon": "plynx.json", "color": "#ffffff"}, {"kind": "executable", "title": "Executable", "cls": "plynx.plugins.resources.common.Executable", "icon": "feathericons.play", "color": "#fcff57"}, {"kind": "directory", "title": "Directory", "cls": "plynx.plugins.resources.common.Directory", "icon": "feathericons.folder", "color": "#f44"}, {"kind": "cloud-storage", "title": "Cloud Storage", "cls": "plynx.plugins.resources.cloud_resources.CloudStorage", "icon": "feathericons.hard-drive", "color": "#5ed1ff"}], "icon": "plynx.kubernetes", "color": "#0f0", "is_static": false}, "k8s-python-node-operation": {"kind": "k8s-python-node-operation", "title": "Kubernetes Python", "executor": "plynx.plugins.executors.kubernetes.PythonNode", "hubs": [], "resources": [{"kind": "file", "title": "File", "cls": "plynx.plugins.resources.common.File", "icon": "feathericons.file", "color": "#fff"}, {"kind": "pdf", "title": "PDF file", "cls": "plynx.plugins.resources.common.PDF", "icon": "plynx.pdf", "color": "#ffffff"}, {"kind": "image", "title": "Image", "cls": "plynx.plugins.resources.common.Image", "icon": "plynx.image", "color": "#ffffff"}, {"kind": "csv", "title": "CSV file", "cls": "plynx.plugins.resources.common.CSV", "icon": "plynx.csv", "color": "#ffffff"}, {"kind": "tsv", "title": "TSV file", "cls": "plynx.plugins.resources.common.TSV", "icon": "plynx.tsv", "color": "#ffffff"}, {"kind": "json", "title": "JSON file", "cls": "plynx.plugins.resources.common.Json", "icon": "plynx.json", "color": "#ffffff"}, {"kind": "executable", "title": "Executable", "cls": "plynx.plugins.resources.common.Executable", "icon": "feathericons.play", "color": "#fcff57"}, {"kind": "directory", "title": "Directory", "cls": "plynx.plugins.resources.common.Directory", "icon": "feathericons.folder", "color": "#f44"}, {"kind": "cloud-storage", "title": "Cloud Storage", "cls": "plynx.plugins.resources.cloud_resources.CloudStorage", "icon": "feathericons.hard-drive", "color": "#5ed1ff"}], "icon": "plynx.kubernetes", "color": "", "is_static": false}, "basic-dag-operation": {"kind": "basic-dag-operation", "title": "Composite Operation", "executor": "plynx.plugins.executors.dag.DAG", "hubs": ["db-hub"], "resources": [{"kind": "file", "title": "File", "cls": "plynx.plugins.resources.common.File", "icon": "feathericons.file", "color": "#fff"}, {"kind": "pdf", "title": "PDF file", "cls": "plynx.plugins.resources.common.PDF", "icon": "plynx.pdf", "color": "#ffffff"}, {"kind": "image", "title": "Image", "cls": "plynx.plugins.resources.common.Image", "icon": "plynx.image", "color": "#ffffff"}, {"kind": "csv", "title": "CSV file", "cls": "plynx.plugins.resources.common.CSV", "icon": "plynx.csv", "color": "#ffffff"}, {"kind": "tsv", "title": "TSV file", "cls": "plynx.plugins.resources.common.TSV", "icon": "plynx.tsv", "color": "#ffffff"}, {"kind": "json", "title": "JSON file", "cls": "plynx.plugins.resources.common.Json", "icon": "plynx.json", "color": "#ffffff"}, {"kind": "executable", "title": "Executable", "cls": "plynx.plugins.resources.common.Executable", "icon": "feathericons.play", "color": "#fcff57"}, {"kind": "directory", "title": "Directory", "cls": "plynx.plugins.resources.common.Directory", "icon": "feathericons.folder", "color": "#f44"}, {"kind": "cloud-storage", "title": "Cloud Storage", "cls": "plynx.plugins.resources.cloud_resources.CloudStorage", "icon": "feathericons.hard-drive", "color": "#5ed1ff"}], "icon": "feathericons.grid", "color": "#5ed1ff", "is_static": false}}, "hubs_dict": {"db-hub": {"kind": "db-hub", "title": "Database hub", "icon": "feathericons.database", "color": "#ffffff", "cls": "plynx.plugins.hubs.collection.CollectionHub", "args": {"operations": ["basic-file", "basic-bash-jinja2-operation", "basic-python-node-operation", "k8s-bash-jinja2-operation", "k8s-python-node-operation", "basic-dag-operation"], "collection": "templates"}}}, "workflows_dict": {"basic-dag-workflow": {"kind": "basic-dag-workflow", "title": "Basic DAG Workflow", "executor": "plynx.plugins.executors.dag.DAG", "operations": [], "hubs": ["db-hub"], "icon": "feathericons.grid", "color": "#5ed1ff"}}, "executors_info": {"basic-dag-workflow": {"is_graph": true, "title": "Basic DAG Workflow", "icon": "feathericons.grid", "color": "#5ed1ff"}, "basic-file": {"is_graph": false, "title": "File", "icon": "feathericons.file", "color": "#fff"}, "basic-bash-jinja2-operation": {"is_graph": false, "title": "BashJinja2 Operation", "icon": "feathericons.terminal", "color": "#0f0"}, "basic-python-node-operation": {"is_graph": false, "title": "Python Operation", "icon": "plynx.python-logo-notext", "color": ""}, "k8s-bash-jinja2-operation": {"is_graph": false, "title": "Kubernetes BashJinja2", "icon": "plynx.kubernetes", "color": "#0f0"}, "k8s-python-node-operation": {"is_graph": false, "title": "Kubernetes Python", "icon": "plynx.kubernetes", "color": ""}, "basic-dag-operation": {"is_graph": true, "title": "Composite Operation", "icon": "feathericons.grid", "color": "#5ed1ff"}, "dummy": {"is_graph": false, "title": "", "icon": "feathericons.grid", "color": "#5ed1ff"}}};

export default class Group extends Component {
  static propTypes = {
    match: PropTypes.shape({
      params: PropTypes.shape({
        group_id: PropTypes.string.isRequired
      }),
    }),
  }

  constructor(props) {
    super(props);
    document.title = "Groups - PLynx";
    this.state = {
      group_id: this.group_id,
      treeData: [
        { title: () => renderHubItem({title: "Chicken", kind: "basic-python-node-operation"}), expanded: true, children: [
            { title: () => renderHubItem({title: "Egg", kind: "basic-bash-jinja2-operation"}) }
        ]},
        { title: () => renderHubItem({title: "Child", kind: "basic-bash-jinja2-operation"}), expanded: false, canExpand: false },
        { title: () => renderHubItem({title: "Egg38", kind: "basic-bash-jinja2-operation"}), expanded: false, canDrop: false, canDrag: false },
        ],
      plugins_dict: PLUGINS_DICT,
    };
  }

  loadGroup(group) {
    this.group = group;
    console.log('resp', group);
    this.setState({
      group: this.group,
    });
  }

  handleSave() {
    this.apiObject.postData({
      group: this.group,
    });
  }

  handlePostResponse(data) {
    if (data.status === RESPONCE_STATUS.SUCCESS) {
      this.apiObject.showAlert('Saved', 'success');
      const refresh = cookie.load('user').username === data.user.username;
      cookie.save('user', data.user, { path: '/' });
      console.log('settings', data.settings);
      cookie.save('settings', data.settings, { path: '/' });
      if (refresh) {
        // Need to reload header if this is the current user
        window.location.reload(false);
      }
    } else {
      this.apiObject.showAlert(data.message, 'failed');
    }
  }

  makeControls() {
    const items = [
      {
        render: makeControlButton,
        props: {
          img: 'save.svg',
          text: 'Save',
          enabled: !this.state.user._readonly,
          func: () => this.handleSave(),
        },
      },
    ];

    return makeControlPanel(
      {
        props: {
          items: items,
          key: 'control',
        },
      });
  }

  handleChangeTree(treeData) {
    console.log(treeData);
    //this.setState({ treeData });
    if (!findError(treeData)) {
      this.setState({ treeData });
    }
  }

  render() {

    return (
      <div className='group-view-content'>
        {false &&
        <APIObject
            collection={COLLECTIONS.GROUPS}
            object_id={this.props.group_id}
            onUpdateData={data => {
              this.loadGroup(data.user);
            }}
            onPostResponse={data => {
              this.handlePostResponse(data);
            }}
            ref={a => this.apiObject = a}
        />
        }
        <PluginsProvider value={this.state.plugins_dict}>
          <div style={{diplay: 'block', height: '100%'}}>
            <SortableTree
              treeData={this.state.treeData}
              onChange={(treeData) => this.handleChangeTree(treeData)}
              //theme={FileExplorerTheme}
            />
          </div>
        </PluginsProvider>
      </div>
    );
  }
}
