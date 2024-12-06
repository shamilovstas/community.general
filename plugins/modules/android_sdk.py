from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_bytes, to_text

from ansible_collections.community.general.plugins.module_utils import cmd_runner_fmt
from ansible_collections.community.general.plugins.module_utils.cmd_runner import CmdRunner


def main():
    module = AnsibleModule(
        argument_spec=dict(
            method=dict(type='str', required=True, choices=['runner', 'manual'])
        )
    )

    sdkmanager = module.get_bin_path('sdkmanager', True)

    method = module.params['method']
    if method == 'runner':
        _state_map = {
            "present": "--install",
            "absent": "--uninstall"
        }
        runner = CmdRunner(module,
                           command='sdkmanager',
                           arg_formats=dict(
                               state=cmd_runner_fmt.as_map(_state_map),
                               name=cmd_runner_fmt.as_list()
                           ),
                           force_lang="C.UTF-8")

        with runner('state name') as ctx:
            rc, stdout, stderr = ctx.run(state="present", name="build-tools;33.0.0")

    else:
        rc, stdout, stderr = module.run_command([sdkmanager, '--install', 'build-tools;34.0.0'])

    if rc != 0:
        module.fail_json(msg="rc not 0 %d: %s" % (rc, stderr))
    else:
        module.exit_json(msg=stdout)


if __name__ == '__main__':
    main()
